from pydantic import BaseModel, Field
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

class GeneratedSymbol(BaseModel):
    updated_symbol_code:str =  Field(description="The full updated code of the symbol being modified, including the symbol declaration and its body. This should be a complete, self-contained code snippet that can be directly used to replace the existing symbol's code in the codebase. Don't include any additional explanations, context or markdown fences, just the raw code.")