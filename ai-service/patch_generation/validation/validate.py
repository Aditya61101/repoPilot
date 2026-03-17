from patch_generation.validation.patch_file_builder import build_patched_file
from patch_generation.validation.semantic_validator import llm_validate_patch
from patch_generation.validation.syntax_validator import validate_file_syntax

def validate_patch_set(issue, repo_state, patch_set):
    # TODO: optimize through parallel validation of patched files
    for patch in patch_set.patches:

        new_lines = build_patched_file(repo_state, patch)
        
        code = "\n".join(new_lines)

        # 1. syntax validation
        ok, error = validate_file_syntax(
            patch.file,
            code
        )
        if not ok:
            print("error while validating syntax:", error)
            return False, {
                "type": "syntax_error",
                "message": error,
                "hint": "Fix syntax errors"
            }

        # 2. semantic validation
        # ok, error = llm_validate_patch(issue, patch.file, code)
        # print("error while doing semantic validation:", error)
        # if not ok:
        #     return False, error

    return True, None