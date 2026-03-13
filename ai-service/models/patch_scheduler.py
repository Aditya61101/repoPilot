from pydantic import BaseModel
from typing import List

class SemanticSchedulerOutput(BaseModel):
    batches: List[List[str]]