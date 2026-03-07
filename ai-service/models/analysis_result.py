from pydantic import BaseModel
from typing import List

class RelevantFile(BaseModel):
    file:str
    reason:str

class AnalysisResult(BaseModel):
    root_cause:str
    relevant_files: List[RelevantFile]
    functions_involved: List[str]
    suggested_edit_files: List[str]
