from pydantic import BaseModel
from typing import Optional, List, Literal

class Patch(BaseModel):
    file: str
    edit_type: Literal['modify', 'insert', 'delete']

    start_line: Optional[int] = None
    end_line: Optional[int] = None

    insert_after_line: Optional[int] = None

    replacement: Optional[str] = None
    content: Optional[str] = None

class PatchSet(BaseModel):
    patches: List[Patch]

