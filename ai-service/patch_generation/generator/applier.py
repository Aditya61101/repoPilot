from models.patch_generator import Patch, PatchSet
from patch_generation.validation.patch_file_builder import build_patched_file

def normalize_patch_set(patch_set):
    # if already an instance of PatchSet
    if hasattr(patch_set, 'patches'):
        return patch_set
    
    patches = []
    for p in patch_set['patches']:
        patches.append(Patch(**p))
    
    return PatchSet(patches=patches)

def apply_patch_set_to_repo_state(repo_state, patch_set):
    
    for patch in patch_set.patches:
        file_path = patch.file
        
        if file_path not in repo_state:
            raise ValueError(f"File {file_path} not found in repo state")
        
        repo_state[file_path] = build_patched_file(repo_state, patch)

        # print(f"new state for {file_path}: ", repo_state[file_path])