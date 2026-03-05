import os 
import faiss
import pickle
import json
from dotenv import load_dotenv
load_dotenv()

VECTOR_STORE = os.getenv("VECTOR_STORE_PATH", "vector_store")
def repo_path(repo):
    return f"{VECTOR_STORE}/{repo.replace("/", "_")}"

def load_metadata(repo):
    path = repo_path(repo)
    with open(f"{path}/metadata.json", "r") as f:
        metadata = json.load(f)
    
    return metadata

def load_index(repo):
    print('inside load_index')
    try:
        path = repo_path(repo)
        index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/chunks.pkl", "rb") as f:
            chunks = pickle.load(f)
        
        metadata = load_metadata(repo)
        
        return index, chunks, metadata
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