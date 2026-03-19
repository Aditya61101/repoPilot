import faiss
from fastapi import APIRouter

from models.request import EnsureIndexedRequest, IndexRequest, AnalyzeRequest, PatchPlannerRequest, PatchGeneratorRequest, StartPipelineRequest, ReviewPipelineRequest

from rag.index_manager import index_exists,  save_index
from rag.embedding import embed_texts

from rag.chunking.parallel_chunking import parallel_chunk

from services.analysis_service import run_issue_analysis
from services.patch_planning_service import patch_planning
from services.patch_generation_service import patch_generation
from services.pipeline_service import review_pipeline, start_pipeline

router = APIRouter(prefix="/ai", tags=['AI'])

@router.post("/ensure-indexed")
def ensure_indexed(req:EnsureIndexedRequest):
    if not index_exists(req.repo_key, req.commit_sha):
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
    if not index_exists(req.repo_key, req.commit_sha):
        return  { "message": "Repo not indexed", "status":False }
    
    analysis = run_issue_analysis(req.repo_key, req.issue, req.commit_sha)

    # print("analysis: ", analysis)
    return {
        "analysis": analysis
    }

@router.post("/plan-patch")
def patch_planner(req:PatchPlannerRequest):
    if not index_exists(req.repo_key, req.commit_sha):
        return  { "message": "Repo not indexed", "status":False }
    
    planned = patch_planning(req.repo_key, req.issue, req.analysis_json, req.commit_sha)
    
    return {
        "patch_plan": planned
    }

@router.post("/generate-patch")
def patch_generator(req:PatchGeneratorRequest):
    if not index_exists(req.repo_key, req.commit_sha):
        return  { "message": "Repo not indexed", "status":False }
    
    response = patch_generation(req.repo_key, req.issue, req.patch_plan, req.commit_sha)
    
    return response



# ----------------- ENDPOINTS FOR ORCHESTRATION -------------------

@router.post("/start")
def invoke_start_pipeline(req:StartPipelineRequest):
    return start_pipeline(
        repo_key=req.repo_key,
        issue=req.issue,
        commit_sha=req.commit_sha
    )

@router.post("/review")
def invoke_review_pipeline(req:ReviewPipelineRequest):
    return review_pipeline(
        thread_id=req.thread_id,
        approved=req.approved,
        feedback=req.feedback
    )