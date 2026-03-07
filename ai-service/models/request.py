from pydantic import BaseModel
from typing import List, Dict
from models.analysis_result import AnalysisResult

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

class PatchPlannerRequest(BaseModel):
    repo_key:str
    issue:str
    analysis_json: dict