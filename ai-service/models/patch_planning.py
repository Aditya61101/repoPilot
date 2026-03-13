from pydantic import BaseModel
from typing import List, Literal

class PatchStep(BaseModel):
    id:str
    file:str
    symbol:str|None
    start_line:int
    end_line:int
    edit_type: Literal['modify', 'insert', 'delete']
    edit_strategy: str
    depends_on: List[str]

class PatchPlan(BaseModel):
    patch_plan: List[PatchStep]