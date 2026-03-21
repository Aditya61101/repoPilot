from pydantic import BaseModel
from typing import List, Dict, Optional


class StartPipelineRequest(BaseModel):
    repo_key:str
    issue: str
    commit_sha:str

class ReviewPipelineRequest(BaseModel):
    thread_id: str
    file_reviews: list

class EnsureIndexedRequest(BaseModel):
    repo_key:str
    commit_sha:str

class IndexRequest(BaseModel):
    repo_key:str
    commit_sha: str
    files: List[Dict[str, str]]

class AnalyzeRequest(BaseModel):
    repo_key:str
    issue:str
    commit_sha:str

class PatchPlannerRequest(BaseModel):
    repo_key:str
    issue:str
    analysis_json: dict
    commit_sha:str

class PatchGeneratorRequest(BaseModel):
    repo_key:str
    issue:str
    patch_plan: list
    commit_sha:str