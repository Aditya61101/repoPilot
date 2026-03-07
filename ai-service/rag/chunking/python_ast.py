
def chunk_python(path, content):
    import ast
    try:
        tree = ast.parse(content)
    except Exception as e:
        print(f"exception occurred while parsing python file: {e}")
        return None
    
    lines = content.splitlines()
    chunks = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno
            end = getattr(node, "end_lineno", start)

            chunk = "\n".join(lines[start-1:end])

            chunks.append({
                "chunk_id": f"{path}:{start}-{end}",
                "path": path,
                "language": "python",
                "symbol": node.name,
                "start_line": start,
                "end_line": end,
                "content": chunk
            })
    return chunks if chunks else None