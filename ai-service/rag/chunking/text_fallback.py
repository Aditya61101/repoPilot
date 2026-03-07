from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.regex import extract_symbol

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

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