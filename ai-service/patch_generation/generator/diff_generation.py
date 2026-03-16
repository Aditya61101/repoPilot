import difflib

def generate_repo_diff(repo_state_before, repo_state_after):

    diffs = []

    all_files = set(repo_state_before.keys()) | set(repo_state_after.keys())

    for file_path in all_files:
        before = repo_state_before.get(file_path, [])
        after = repo_state_after.get(file_path, [])

        if before == after:
            continue

        diff = difflib.unified_diff(
            before,
            after,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm=""
        )

        diffs.append("\n".join(diff))
    
    return "\n".join(diffs)