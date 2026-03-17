from pydantic import BaseModel
from typing import Literal, Optional

class ValidationResult(BaseModel):
    status: Literal["PASS", "FAIL"]
    type: Optional[str] = None
    message: Optional[str] = None
    hint: Optional[str] = None