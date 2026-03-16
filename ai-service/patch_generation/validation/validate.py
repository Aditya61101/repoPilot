from patch_generation.validation.patch_file_builder import build_patched_file
from patch_generation.validation.syntax_validator import validate_file_syntax

def validate_patch_set(repo_state, patch_set):
    # TODO: optimize through parallel validation of patched files
    for patch in patch_set.patches:

        new_lines = build_patched_file(repo_state, patch)
        
        code = "\n".join(new_lines)
        ok, error = validate_file_syntax(
            patch.file,
            code
        )

        if not ok:
            return False, error

    return True, ""