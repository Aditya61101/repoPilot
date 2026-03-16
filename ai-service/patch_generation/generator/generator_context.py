# PATCH_CONTEXT_WINDOW = 15


# def extract_patch_context(file_chunks, step):
#     """
#     Extracts code context around the patch region.
#     """
    
#     path=step['file']
#     start_line=step['start_line']
#     end_line=step['end_line']

#     chunks = file_chunks.get(path)
#     if not chunks:
#         return ""

#     context_chunks = []

#     for c in chunks:
#         if (
#             c["end_line"] >= start_line - PATCH_CONTEXT_WINDOW
#             and c["start_line"] <= end_line + PATCH_CONTEXT_WINDOW
#         ):  
#             context_chunk = f"""
#             // FILE: {path}
#             // LINES:
#             {c['start_line']}-{c['end_line']}

#             {c["content"]}
#             """
            
#             context_chunks.append(context_chunk)

#     return "\n".join(context_chunks)


def resolve_dependencies(step, patch_lookup):
    visited = set()
    stack = list(step.get("depends_on", []))

    while stack:
        dep = stack.pop()
        if dep in visited or dep == []:
            continue
        
        visited.add(dep)
        parent = patch_lookup[dep]
        stack.extend(parent.get('depends_on', []))
    
    return visited

def extract_dependency_context(step, patch_lookup, patch_results):
    context = []

    dep_ids = resolve_dependencies(step, patch_lookup)

    for dep_id in dep_ids:
        patch_set = patch_results.get(dep_id)
        
        if not patch_set:
            continue

        for patch in patch_set.patches:
            snippet = patch.replacement or patch.content or  ""

            context.append(
                f"""
                DEPENDENCY PATCH RESULT
                PATCH: {dep_id}
                FILE: {patch.file}

                ```code
                {snippet}
                """
            )
    
    return "\n".join(context)