from patch_generation.validation.patch_file_builder import build_patched_file

def apply_patch_set_to_repo_state(repo_state, patch_set):
    
    for patch in patch_set.patches:
        file_path = patch.file
        
        if file_path not in repo_state:
            raise ValueError(f"File {file_path} not found in repo state")
        
        repo_state[file_path] = build_patched_file(repo_state, patch)