from patch_generation.validation.patch_file_builder import build_patched_file
from patch_generation.validation.syntax_validator import validate_file_syntax

def validate_patch_set(repo_state, patch_set):
    # TODO: optimize through parallel validation of patched files
    for patch in patch_set.patches:

        new_file_code = build_patched_file(repo_state, patch)
        print("new code file: ", new_file_code)
        ok, error = validate_file_syntax(
            patch.file,
            new_file_code
        )

        if not ok:
            return False, error

    return True, ""