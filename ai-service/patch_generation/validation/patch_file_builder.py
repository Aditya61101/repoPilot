def build_patched_file(repo_state, patch):

    lines = repo_state[patch.file]

    start = patch.start_line - 1
    end = patch.end_line

    replacement = patch.replacement.splitlines()
    print("Replacement lines: ", replacement)
    new_lines = (
        lines[:start] +
        replacement +
        lines[end:]
    )

    return "\n".join(new_lines)