from concurrent.futures import ThreadPoolExecutor
from rag.chunking.chunk_file import chunk_file
from utils.language_detection import detect_language
from utils.regex import extract_imports

def process_file(file_obj):
    path = file_obj['path']
    print(f"processing file for path: {path}")
    print("------------------------------------")
    content = file_obj['content']
    lang = detect_language(path)
    imports = extract_imports(content, lang)
    
    print(f"imports extracted: {imports}")
    print("------------------------------------")
    
    file_chunks = chunk_file(path, content)
    for c in file_chunks:
        c['imports'] = imports
    
    print(f"file chunking completed for path: {path}")
    print("------------------------------------")
    
    return file_chunks

def parallel_chunk(files):
    print("inside parallel chunk")
    print("------------------------------------")
    chunks = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_file, files)

        for file_chunks in results:
            chunks.extend(file_chunks)

    return chunks