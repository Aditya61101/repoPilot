
from models.patch_validator import ValidationResult
from utils.llm_client import set_llm

validator_llm = set_llm().with_structured_output(ValidationResult)
def llm_validate_patch(issue, file_path, code):
    # print("code given for validation: ", code)
    prompt = f"""
You are a senior engineer reviewing a code patch.

ISSUE:
{issue}

CODE:
{code}

Check:
- correctness
- logic errors
- API misuse
- completeness

Return:
- PASS if correct
- FAIL if incorrect with type, message, hint
"""

    result: ValidationResult = validator_llm.invoke(prompt)
    if result.status == "FAIL":
        return False, result.model_dump()

    return True, None