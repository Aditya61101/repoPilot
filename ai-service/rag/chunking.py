from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.regex import extract_symbol
from utils.language_detection import detect_language

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

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

def split_code_blocks(path, content, lang):
    chunks = []
    stack = []
    start_char = None
    lines = content.splitlines()

    char_to_line = []
    line = 1
    for c in content:
        char_to_line.append(line)
        if c == "\n":
            line+=1
    
    for i, ch in enumerate(content):
        if ch == "{":
            if not stack:
                start_char = i
            stack.append("{")
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start_char is not None:
                    end_char = i
                    start_line = char_to_line[start_char]
                    end_line = char_to_line[end_char]
                    chunk_text = "\n".join(lines[start_line-1:end_line])
                    chunks.append({
                        "chunk_id": f"{path}:{start_line}-{end_line}",
                        "path": path,
                        "language": lang,
                        "symbol": extract_symbol(chunk_text, lang), 
                        "start_line": start_line,
                        "end_line": end_line,
                        "content": chunk_text
                    })
    return chunks if chunks else None

def chunk_text_fallback(path, content, lang):
    chunks = []
    text_chunks = splitter.split_text(content)
    curr_line = 1

    for chunk in text_chunks:
        chunk_lines = chunk.count("\n")+1
        start_line = curr_line
        end_line = curr_line + chunk_lines-1

        chunks.append({
            "chunk_id": f"{path}:{start_line}-{end_line}",
            "path": path,
            "language": lang,
            "symbol": extract_symbol(chunk, lang),
            "start_line":start_line,
            "end_line": end_line,
            "content": chunk
        })
        curr_line = end_line+1
    return chunks

def chunk_file(path, content):
    
    lang = detect_language(path)
    # smaller content need no chunking
    if len(content) < 400:
        lines = content.splitlines()
        return  [{
            "chunk_id": f"{path}:1-{len(lines)}",
            "path": path, 
            "language": lang,
            "symbol": extract_symbol(content, lang),
            "start_line":1,
            "end_line": len(lines),
            "content": content
        }]
    
    if lang == 'python':
        chunks = chunk_python(path, content)
        if chunks: 
            return chunks

    blocks = split_code_blocks(path, content, lang)
    if blocks:
        return blocks

    return chunk_text_fallback(path, content, lang)
