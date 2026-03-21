import uuid

from fastapi import HTTPException
from langgraph.types import Command
from orchestration.builder import build_graph
from orchestration.checkpoint import get_checkpointer

checkpointer = get_checkpointer()
graph = build_graph(checkpointer)

def start_pipeline(repo_key, issue, commit_sha):
    thread_id = f"{repo_key}:{uuid.uuid4()}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    initial_state = {
        "repo_key": repo_key,
        "issue": issue,
        "commit_sha": commit_sha
    }

    for event in graph.stream(
        initial_state,
        config=config
    ):
        for node_name, _ in event.items():
            print(f"[NODE NAME] -> {node_name}")
    state = graph.get_state(config)
    if not state.next or state.next[0] != 'review':
        raise HTTPException(500, detail=f'Pipeline ended unexpectedly at: {state.next}')
    
    return {
        "thread_id": thread_id,
        "file_diffs": state.values['file_diffs']
    }

def review_pipeline(thread_id, file_reviews):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    state = graph.get_state(config)
    if state is None:
        raise HTTPException(404, detail='Thread not found')
    
    if not state.next or state.next[0]!='review':
        raise HTTPException(409, detail=f"Thread is not awaiting review (next={state.next})")
    
    resume_state = {
        "file_reviews": file_reviews
    }
    for event in graph.stream(
        Command(resume=resume_state),
        config=config
    ):
        for node_name, _ in event.items():
            print(f"[PIPELINE] -> {node_name}")
    
    final_state = graph.get_state(config)
    # suspended again at review -> another rejection loop
    if final_state.next and final_state.next[0] == 'review':
        return {
            "thread_id": thread_id,
            "file_diffs": final_state.values['file_diffs']
        }
    # graph ran to END -> PR was opened
    return {
        "pr_url": final_state.values['pr_url']
    }