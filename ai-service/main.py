import faiss
from fastapi import FastAPI
from models.request import EnsureIndexedRequest, IndexRequest, AnalyzeRequest
from rag.index_manager import index_exists, load_metadata, save_index
from rag.retreiver import retrieve
from rag.embedding import embed_texts
from util.parallel_chunking import parallel_chunk

app = FastAPI()

@app.post("/ensure-indexed")
def ensure_indexed(req:EnsureIndexedRequest):
    if not index_exists(req.repo_key):
        return { "needs_index": True }
    
    metadata = load_metadata(req.repo_key)
    if metadata['commit_sha'] != req.commit_sha:
        return { "needs_index": True }

    return { "needs_index": False }

@app.post("/index")
def index_repo(req:IndexRequest):
    chunks = parallel_chunk(req.files)

    texts = [f"FILE: {c['path']}\nLANGUAGE: {c['language']}\nSYMBOL: {c.get('symbol')}\n\n{c['content']}" for c in chunks]
    
    embeddings = embed_texts(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    # normalizes embeddings: converts vectors to unit length
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    res = save_index(
        repo=req.repo_key,
        index=index,
        chunks=chunks, 
        commit_sha=req.commit_sha
    )

    return {
        "message": "Repo indexed" if res else "Repo indexing failed", 
        "chunks":len(chunks) if res else 0, 
        "status": res
    }

@app.post("/analyze")
def analyze(req:AnalyzeRequest):
    if not index_exists(req.repo_key):
        return  { "message": "Repo not indexed", "status":False }
    
    grouped_chunks = retrieve(
        req.repo_key, 
        req.issue, 
        k=30
    )

    print("relevant chunks: ", grouped_chunks)
    # for now we return context, later we will feed this context to LLM
    return {
        "retrieved_context": grouped_chunks
    }
