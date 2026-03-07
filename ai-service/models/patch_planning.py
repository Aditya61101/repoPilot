from pydantic import BaseModel
from typing import List, Literal

class PatchStep(BaseModel):
    file:str
    symbol:str|None
    start_line:int
    end_line:int
    edit_type: Literal['modify', 'add', 'remove']
    reason:str

class PatchPlan(BaseModel):
    patch_plan: List[PatchStep]