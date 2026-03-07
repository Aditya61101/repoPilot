from utils.regex import extract_symbol
from utils.language_detection import detect_language
from rag.chunking.python_ast import chunk_python
from rag.chunking.symbol_chunking import split_by_symbols
from rag.chunking.text_fallback import chunk_text_fallback

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

    blocks = split_by_symbols(path, content, lang)
    if blocks:
        return blocks

    return chunk_text_fallback(path, content, lang)