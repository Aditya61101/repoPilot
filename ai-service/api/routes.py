import faiss
from fastapi import APIRouter

from models.request import EnsureIndexedRequest, IndexRequest, AnalyzeRequest, PatchPlannerRequest, PatchGeneratorRequest

from rag.index_manager import index_exists, load_metadata, save_index
from rag.embedding import embed_texts

from rag.chunking.parallel_chunking import parallel_chunk

from services.analysis_service import run_issue_analysis
from services.patch_planning_service import patch_planning
from services.patch_generation_service import patch_generation

router = APIRouter(prefix="/ai", tags=['AI'])

@router.post("/ensure-indexed")
def ensure_indexed(req:EnsureIndexedRequest):
    if not index_exists(req.repo_key):
        return { "needs_index": True }
    
    metadata = load_metadata(req.repo_key)
    if metadata['commit_sha'] != req.commit_sha:
        return { "needs_index": True }

    return { "needs_index": False }

@router.post("/index")
def index_repo(req:IndexRequest):
    chunks = parallel_chunk(req.files)

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
        repo=req.repo_key,
        index=index,
        chunks=chunks, 
        commit_sha=req.commit_sha,
        files=req.files
    )

    return {
        "message": "Repo indexed" if res else "Repo indexing failed", 
        "chunks":len(chunks) if res else 0, 
        "status": res
    }

@router.post("/analyze")
def analyze(req:AnalyzeRequest):
    if not index_exists(req.repo_key):
        return  { "message": "Repo not indexed", "status":False }
    
    analysis = run_issue_analysis(req.repo_key, req.issue)

    # print("analysis: ", analysis)
    return {
        "analysis": analysis
    }

@router.post("/plan-patch")
def patch_planner(req:PatchPlannerRequest):
    if not index_exists(req.repo_key):
        return  { "message": "Repo not indexed", "status":False }
    
    planned = patch_planning(req.repo_key, req.issue, req.analysis_json)
    
    # print("planned patch: ", planned)
    return planned

@router.post("/generate-patch")
def patch_generator(req:PatchGeneratorRequest):
    if not index_exists(req.repo_key):
        return  { "message": "Repo not indexed", "status":False }
    
    patches = patch_generation(req.repo_key, req.issue, req.patch_plan)
    
    # print("generated patch: ", patches)
    return patches
