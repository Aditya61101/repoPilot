import os

import faiss
import requests

from copy import deepcopy

from models.patch_generator import PatchSet
from orchestration.state import GraphState
from patch_generation.generator.applier import apply_patch_set_to_repo_state, normalize_patch_set
from patch_generation.generator.diff_generation import generate_repo_diff
from rag.chunking.parallel_chunking import parallel_chunk
from rag.embedding import embed_texts
from rag.index_manager import get_index, index_exists, save_index
from services.analysis_service import run_issue_analysis
from services.patch_generation_service import patch_generation
from services.patch_planning_service import patch_planning
from services.pr_service import create_pull_request

def check_index_node(state:GraphState):
    print("state in check index node: ", state)
    repo_key = state['repo_key']
    commit_sha = state['commit_sha']

    state['is_indexed'] = index_exists(repo_key, commit_sha)
    return state
    
def index_node(state:GraphState):
    repo_key = state['repo_key']
    commit_sha = state['commit_sha']

    url = f'{os.getenv('API_SERVICE_BASE_URL')}/v2/files/{repo_key}/{commit_sha}'

    response = requests.get(url=url)
    files = response.json()

    chunks = parallel_chunk(files)

    texts = [f"FILE: {c['path']}\nLANGUAGE: {c['language']}\nSYMBOL: {c.get('symbol')}\n\n{c['content']}" for c in chunks]
    
    embeddings = embed_texts(texts)

    print("embedding completed")
    print("------------------------------------")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    
    # normalizes embeddings: converts vectors to unit length
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    print("index added")
    print("------------------------------------")

    res = save_index(
        repo=repo_key,
        index=index,
        chunks=chunks, 
        commit_sha=commit_sha,
        files=files
    )
    print("repo indexed?:", res)
    return state

def analyze_node(state:GraphState):
    state['analysis'] = run_issue_analysis(
        state['repo_key'], 
        state['issue'],
        state['commit_sha']
    )
    return state

def plan_node(state:GraphState):
    state['patch_plan'] = patch_planning(
        state['repo_key'], 
        state['issue'], 
        state['analysis'],
        state['commit_sha']
    )
    return state

def generate_node(state:GraphState):
    state['patch_set'] = patch_generation(
        state['repo_key'], 
        state['issue'],
        state['patch_plan'],
        state['commit_sha']
    )
    return state


def diff_node(state:GraphState):
    # print("patches: ", state['patch_set'])
    repo_index = get_index(
        state['repo_key'], 
        state['commit_sha']
    )

    original_repo_state = repo_index['repo_state']

    patched_repo_state = deepcopy(original_repo_state)
    
    patch_set = normalize_patch_set(state['patch_set'])
    apply_patch_set_to_repo_state(
        patched_repo_state, 
        patch_set
    )

    state['diff'] = generate_repo_diff(
        original_repo_state,
        patched_repo_state
    )
    return state

def review_node(state:GraphState):
    return state

def regenerate_node(state:GraphState):
    # TODO: use feedback
    state['patch_set'] = patch_generation(
        state['repo_key'], 
        state['issue'],
        state['patch_plan']
    )
    return state

def pr_node(state:GraphState):
    repo_state = get_index(state['repo_key'], state['commit_sha'])['repo_state']

    patch_set = normalize_patch_set(state['patch_set'])
    
    apply_patch_set_to_repo_state(
        repo_state,
        patch_set
    )
    
    state['pr_url'] = create_pull_request(
        repo_state,
        patch_set,
        state['repo_key'],
        base_branch="main"
    )
    return state