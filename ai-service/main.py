from fastapi import FastAPI
from models.request import EnsureIndexedRequest, IndexRequest, AnalyzeRequest

app = FastAPI()

# in memory storage for now
repo_store = {}

@app.post("/ensure-indexed")
def ensure_indexed(req:EnsureIndexedRequest):
    if req.repo_key not in repo_store:
        return {"needs_index": True}

    if repo_store[req.repo_key]['commit_sha'] != req.commit_sha:
        return {"needs_index": True}

    return {"needs_index": False}

@app.post("/index")
def index_repo(req:IndexRequest):
    repo_store[req.repo_key] = {
        "commit_sha": req.commit_sha,
        "files": req.files
    }
    print("repo store: ", repo_store)
    return  {"status": "indexed"}

@app.post("/analyze")
def analyze(req:AnalyzeRequest):
    if req.repo_key not in repo_store:
        return  {"error": "Repo not indexed"}
    
    files = repo_store[req.repo_key]['files']

    return {
        "analysis": f"Issue received: {req.issue}\nIndexed files count: {len(files)}"
    }
