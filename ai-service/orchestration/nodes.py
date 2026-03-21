import os
import requests

from copy import deepcopy
from langgraph.types import interrupt
from orchestration.state import GraphState
from patch_generation.generator.applier import apply_patch_set_to_repo_state, normalize_patch_set
from rag.index_manager import get_index, index_exists
from rag.main import index_entry_point
from services.analysis_service import run_issue_analysis
from services.patch_generation_service import patch_generation
from services.patch_planning_service import patch_planning
from services.pr_service import create_pull_request
from utils.language_detection import detect_language
# from patch_generation.generator.diff_generation import generate_repo_diff

def check_index_node(state:GraphState):
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

    res, _ = index_entry_point(
        repo_key=repo_key,
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
    result = patch_generation(
        state['repo_key'], 
        state['issue'],
        state['patch_plan'],
        state['commit_sha']
    )
    state['patch_set'] = result['patch_set']
    state['patch_results'] = result['patch_results']
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

    file_diffs = []
    for file_path in patched_repo_state:
        original_code = original_repo_state[file_path]
        updated_code = patched_repo_state[file_path]

        if original_code != updated_code:
            file_diffs.append({
                "file": file_path,
                "language": detect_language(file_path),
                "original": "\n".join(original_code),
                "modified": "\n".join(updated_code)
            })
    
    state['file_diffs'] = file_diffs

    return state

def review_node(state:GraphState):
    # return state
    human_input = interrupt({
        "file_diffs": state['file_diffs']
    })

    return {
        **state,
        "file_reviews": human_input['file_reviews']
    }

def regenerate_node(state:GraphState):
    repo_index = get_index(
        state['repo_key'], 
        state['commit_sha']
    )
    repo_state = repo_index['repo_state']
    updated_repo_state = deepcopy(repo_state)

    patch_set = normalize_patch_set(state['patch_set'])
    apply_patch_set_to_repo_state(
        updated_repo_state,
        patch_set
    )
    
    feedback_map = {
        f['file']: f['feedback'] for f in state['file_reviews'] if not f['approved']
    }
    target_files = set(feedback_map.keys())

    result = patch_generation(
        state['repo_key'], 
        state['issue'],
        state['patch_plan'],
        state['commit_sha'],
        updated_repo_state,
        target_files=target_files,
        feedback_map=feedback_map,
        existing_patch_results=state['patch_results']
    )
    state['patch_set'] = result['patch_set']
    state['patch_results'] = result['patch_results']
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