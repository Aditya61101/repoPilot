from concurrent.futures import ThreadPoolExecutor
from rag.chunking import chunk_file

def process_file(file_obj):
    path = file_obj['path']
    content = file_obj['content']
    return chunk_file(path, content)

def parallel_chunk(files):
    chunks = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(process_file, files)

        for file_chunks in results:
            chunks.extend(file_chunks)

    return chunks