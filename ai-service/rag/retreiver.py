import re
import faiss
from collections import defaultdict
from rag.embedding import embed_query
from rag.index_manager import get_index
from constants import MAX_TOKEN

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

def keyword_score(retrieved_chunk, query):
    text = (retrieved_chunk['content']+retrieved_chunk['path']).lower()

    score = 0
    for w in query:
        if w in text:
            score+=1
    return score

def symbol_score(retrieved_chunk, query):
    symbol = retrieved_chunk.get("symbol")
    if not symbol:
        return 0
    
    symbol = symbol.lower()
    score = 0
    for w in query:
        if w in symbol:
            score+= 1
    return score

def expand_context(top_chunks, file_chunks, window=1):
    expanded = []
    for chunk in top_chunks:
        path = chunk['path']
        # get chunks from same file
        same_file_chunks = file_chunks[path]
        idx = same_file_chunks.index(chunk)

        start = max(0, idx-window)
        end = min(len(same_file_chunks), idx+window+1)

        expanded.extend(same_file_chunks[start:end])
    
    # deduplicate
    unique = {}
    for c in expanded:
        key = (c['path'], c['start_line'])
        unique[key] = c

    return list(unique.values())

def retrieve(repo, query:str, k=5):
    repo_index = get_index(repo=repo)
    index = repo_index['index']
    chunks = repo_index['chunks']
    file_chunks = repo_index['file_chunks']

    query_vector = embed_query(query)
    faiss.normalize_L2(query_vector)
    
    D, I = index.search(query_vector, k)
    print("Distance: ", D)
    print("vector ids: ", I)

    # chat streaming -> ['chat', 'streaming']
    query_words = re.findall(r"\w+", query.lower())
    results = []

    for rank, idx in enumerate(I[0]):
        chunk = chunks[idx]

        semantic_score =  1/(1+D[0][rank])
        k_score = keyword_score(chunk, query_words)
        s_score = symbol_score(chunk, query_words)
        # will be replaced by Reciprocal Rank Fusion (RRF)
        final_score = (
            0.7 * semantic_score
            + 0.2 * k_score
            + 0.1 * s_score
        )
        if k_score==0:
            final_score*=0.5
        results.append((final_score, chunk))

    # re rank: sorting on the basis of final_score per chunk
    results.sort(reverse=True, key=lambda x:x[0])
    
    # top chunks
    top_chunks = [c for _,c in results[:10]]
    
    # context expansion
    top_expanded_chunks = expand_context(top_chunks=top_chunks, file_chunks=file_chunks)
    
    # grouping chunks by file
    grouped = defaultdict(list)
    for chunk in top_expanded_chunks:
        grouped[chunk['path']].append(chunk)
    
    # expanding based on imports
    grouped = expand_imports(grouped=grouped, file_chunks=file_chunks)

    # packing
    packed = pack_context(grouped_chunks=grouped, max_tokens=MAX_TOKEN)

    return packed