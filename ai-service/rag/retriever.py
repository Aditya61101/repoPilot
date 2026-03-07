import faiss
from collections import defaultdict
from rag.embedding import embed_query
from rag.index_manager import get_index
from rag.models import get_reranker
from rag.graph.graph_expander import expand_graph
from constants import MAX_TOKEN, RETRIEVAL_CONFIG, K_RRF
from utils.regex import TOKEN_PATTERN

# this assumes 1 token = 4 chars
def estimate_tokens(text):
    return max(1, len(text)//4)

# token aware packing to avoid token limit exceed
def pack_context(grouped_chunks:dict, max_tokens=12000):
    packed = {}
    used_tokens = 0

    for path, chunks in grouped_chunks.items():
        packed_chunks = []
        for chunk in chunks:
            token_cost = estimate_tokens(chunk['content'])

            if used_tokens + token_cost > max_tokens:
                return packed

            packed_chunks.append(chunk)
            used_tokens+=token_cost

        if packed_chunks:
            packed[path] = packed_chunks
    return packed

def expand_imports(grouped, file_chunks, max_import_files=2):
    expanded = dict(grouped)
    added = 0
    for _, chunks in grouped.items():
        imports = chunks[0].get("imports", [])

        for imp in imports:
            if added >= max_import_files:
                return expanded
            for candidate_file in file_chunks:
                if imp in candidate_file and candidate_file not in expanded:
                    expanded[candidate_file] = file_chunks[candidate_file]
                    added+=1
                    break
    return expanded

def expand_context(top_chunks, file_chunks, window=1):
    expanded = []
    for chunk in top_chunks:
        path = chunk['path']
        # get chunks from same file
        same_file_chunks = file_chunks[path]
        idx = chunk['file_index']

        start = max(0, idx-window)
        end = min(len(same_file_chunks), idx+window+1)

        expanded.extend(same_file_chunks[start:end])
    
    # deduplicate
    unique = []
    seen = set()
    for c in expanded:
        key = c['chunk_id']
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique

def retrieve(repo, query:str, stage:str):

    config = RETRIEVAL_CONFIG[stage]

    dense_k = config['dense_k']
    sparse_k = config['sparse_k']
    window = config['window']
    graph_depth = config['graph_depth']
    rerank_top = config['rerank_top']

    repo_index = get_index(repo=repo)
    index = repo_index['index']
    chunks = repo_index['chunks']
    file_chunks = repo_index['file_chunks']
    bm25 = repo_index['bm25']
    repo_graph = repo_index['repo_graph']

    query_vector = embed_query(query)
    faiss.normalize_L2(query_vector)
    ### dense retrieval
    D, I_dense = index.search(query_vector, dense_k)
    dense_chunks = [chunks[i] for i in I_dense[0]]
    
    ### sparse retrieval
    # chat streaming -> ['chat', 'streaming']
    query_words = TOKEN_PATTERN.findall(query.lower())
    bm25_scores = bm25.get_scores(query_words)
    top_sparse = sorted(
        enumerate(bm25_scores),
        key=lambda x:x[1],
        reverse=True
    )[:sparse_k]
    sparse_chunks = [chunks[i] for i,_ in top_sparse]
    
    ### reciprocal rank fusion
    rrf_scores = defaultdict(float)
    for rank, chunk in enumerate(dense_chunks, 1):
        cid = chunk['chunk_id']
        rrf_scores[cid]+=1/(K_RRF+rank)
    
    for rank, chunk in enumerate(sparse_chunks, 1):
        cid = chunk['chunk_id']
        rrf_scores[cid]+=1/(K_RRF+rank)
    
    candidate_chunks = {
        c['chunk_id']: c for c in dense_chunks+sparse_chunks
    }
    fused = [
        (score, candidate_chunks[cid]) for cid, score in rrf_scores.items()
    ]
    fused.sort(reverse=True, key=lambda x:x[0])
    top_candidates = [c for _,c in fused[:rerank_top]]
    
    ### cross encoder reranking
    pairs = [
        (
            query,
            f"""
            File: {c['path']}
            Function: {c.get('symbol')}
            Imports: {",".join(c.get('imports', []))}
            Code: {c['content']}
            """
        ) for c in top_candidates
    ]
    reranker = get_reranker()
    scores = reranker.predict(pairs, batch_size=8)
    reranked = sorted(
        zip(scores, top_candidates),
        reverse=True
    )
    top_chunks = [c for _,c in reranked[:8]]
    
    ### context expansion
    top_expanded_chunks = expand_context(
        top_chunks=top_chunks, 
        file_chunks=file_chunks,
        window=window
    )
    
    ### grouping chunks by file
    grouped = defaultdict(list)
    for chunk in top_expanded_chunks:
        grouped[chunk['path']].append(chunk)
    
    ### packing
    packed = pack_context(grouped_chunks=grouped, max_tokens=MAX_TOKEN)

    ### expanding based on repo graph
    expanded_files = expand_graph(
        files=list(packed.keys()),
        repo_graph=repo_graph,
        limit=graph_depth
    )
    for f in expanded_files:
        if f not in packed:
            packed[f] = [file_chunks[f][0]]

    return packed