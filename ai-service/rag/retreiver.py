import re
import faiss
from collections import defaultdict
from rag.embedding import embed_query
from rag.index_manager import load_index

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
    for w in query:
        if w in symbol:
            return 1
    return 0

def retrieve(repo, query:str, k=5):
    index, chunks, _  = load_index(repo=repo)

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

        final_score = (
            0.7 * semantic_score
            + 0.2 * k_score
            + 0.1 * s_score
        )
        results.append((final_score, chunk))

    # re rank: sorting on the basis of final_score per chunk
    results.sort(reverse=True, key=lambda x:x[0])
    # top chunks
    top_chunks = [c for _,c in results[:10]]
    # grouping chunks by file
    grouping = defaultdict(list)
    for chunk in top_chunks:
        grouping[chunk['path']].append(chunk)

    return grouping