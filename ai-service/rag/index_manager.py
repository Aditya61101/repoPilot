import os 
import faiss
import pickle
import json
from rank_bm25 import BM25Okapi
from functools import lru_cache
from dotenv import load_dotenv
from utils.regex import TOKEN_PATTERN
load_dotenv()

VECTOR_STORE = os.getenv("VECTOR_STORE_PATH", "vector_store")
def repo_path(repo):
    return f"{VECTOR_STORE}/{repo.replace("/", "_")}"

def load_metadata(repo):
    path = repo_path(repo)
    with open(f"{path}/metadata.json", "r") as f:
        metadata = json.load(f)
    
    return metadata

# in memory caching
index_cache = {}
def get_index(repo):
    if repo in index_cache:
        print("loading index from memory cache")
        return index_cache[repo]
    index, chunks, metadata, file_chunks, bm25 = load_index(repo=repo)

    index_cache[repo] = {
        "index": index,
        "chunks": chunks,
        "metadata": metadata,
        "file_chunks": file_chunks,
        "bm25": bm25
    }
    print("loading index from disk")
    return index_cache[repo]

def load_index(repo):
    print('inside load_index')
    try:
        path = repo_path(repo)
        index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/chunks.pkl", "rb") as f:
            chunks = pickle.load(f)
        
        metadata = load_metadata(repo)
        
        from collections import defaultdict

        # grouping file by path
        file_chunks = defaultdict(list)
        for c in chunks:
            file_chunks[c['path']].append(c)
        # sorting each file content by start_line
        for c_in_file in file_chunks.values():
            c_in_file.sort(key=lambda x: x['start_line'])
        # building BM25
        corpus = [
            TOKEN_PATTERN.findall(
                f"{c['path']} {c.get('symbol', '')} {c['content']}".lower()
            ) for c in chunks
        ]
        bm25 = BM25Okapi(corpus)

        return index, chunks, metadata, file_chunks, bm25
    except Exception as e:
        print('loading existing index failed', e)
        return None

def save_index(repo, index, chunks, commit_sha):
    print('inside save_index')
    try:
        path = repo_path(repo)
        os.makedirs(path, exist_ok=True)

        print("writing index.faiss")
        faiss.write_index(index, f"{path}/index.faiss")
        print("index.faiss writing completed")

        print("writing chunks.pkl")
        with open(f"{path}/chunks.pkl", "wb") as f:
            pickle.dump(chunks, f)
        print("chunks.pkl writing completed")
        # writing metadata for the index
        metadata = {
            "commit_sha": commit_sha,
            "chunk_count": len(chunks)
        }
        with open(f"{path}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        return True
    except Exception as e:
        print('index saving failed', e)
        return False

def index_exists(repo):
    path = repo_path(repo)
    return os.path.exists(f"{path}/index.faiss")