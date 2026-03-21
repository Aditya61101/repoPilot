import faiss

from rag.chunking.parallel_chunking import parallel_chunk
from rag.embedding import embed_texts
from rag.index_manager import save_index

def index_entry_point(
    repo_key, 
    commit_sha, 
    files
):
    chunks = parallel_chunk(files)

    texts = [f"FILE: {c['path']}\nLANGUAGE: {c['language']}\nSYMBOL: {c.get('symbol')}\n\n{c['content']}" for c in chunks]
    
    embeddings = embed_texts(texts)

    print("embedding completed")
    print("------------------------------------")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    
    # normalizes embeddings: converts vectors to unit length
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    print("index added")
    print("------------------------------------")

    res = save_index(
        repo=repo_key,
        index=index,
        chunks=chunks, 
        commit_sha=commit_sha,
        files=files
    )

    return res, chunks