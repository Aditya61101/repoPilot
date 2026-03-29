from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.request import EnsureIndexedRequest, IndexRequest, AnalyzeRequest, PatchPlannerRequest, PatchGeneratorRequest, StartPipelineRequest, ReviewPipelineRequest

from rag.index_manager import index_exists

from rag.main import index_entry_point
from services.analysis_service import run_issue_analysis
from services.patch_planning_service import patch_planning
from services.patch_generation_service import patch_generation
from services.pipeline_service import review_pipeline, review_pipeline_v2, start_pipeline, start_pipeline_v2, stream_pipeline

router = APIRouter(prefix="/ai", tags=['AI'])

@router.post("/ensure-indexed")
def ensure_indexed(req:EnsureIndexedRequest):
    if not index_exists(req.repo_key, req.commit_sha):
        return { "needs_index": True }
    return { "needs_index": False }

@router.post("/index")
def index_repo(req:IndexRequest):
    res, chunks = index_entry_point(
        repo_key=req.repo_key,
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
        file_reviews=req.file_reviews
    )

@router.post("/v2/start")
def invoke_start_pipeline_v2(body: StartPipelineRequest):
    return start_pipeline_v2(
        repo_key=body.repo_key,
        issue=body.issue,
        commit_sha=body.commit_sha,
    )

@router.get("/v2/{thread_id}/stream")
async def stream(thread_id: str) -> StreamingResponse:
    return await stream_pipeline(thread_id)

@router.post("/v2/{thread_id}/review")
def review(req: ReviewPipelineRequest):
    return review_pipeline_v2(
        thread_id=req.thread_id,
        file_reviews=req.file_reviews,
    )