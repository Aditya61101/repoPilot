import asyncio
import json
import threading
import uuid

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from langgraph.types import Command
from orchestration.builder import build_graph
from orchestration.checkpoint import get_checkpointer

checkpointer = get_checkpointer()
graph = build_graph(checkpointer)

def _run_graph(initial_state:dict, config:dict):
    for event in graph.stream(initial_state, config=config):
        for node_name, _ in event.items():
            print(f"[NODE NAME] -> {node_name}")

def _resume_graph(config:dict, file_reviews:dict):
    for event in graph.stream(
        Command(resume={"file_reviews": file_reviews}),
        config=config
    ):
        for node_name, _ in event.items():
            print(f"[PIPELINE] -> {node_name}")

def start_pipeline_v2(repo_key, issue, commit_sha) -> dict:
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

    threading.Thread(
        target=_run_graph,
        args=(initial_state,config)
    ).start()

    return {"thread_id": thread_id}

def review_pipeline_v2(thread_id:str, file_reviews:dict) -> dict:
    config = {"configurable": {"thread_id": thread_id}}

    state = graph.get_state(config)
    if state is None:
        raise HTTPException(404, detail='Thread not found')
    
    if not state.next or state.next[0]!='review':
        raise HTTPException(409, detail=f"Thread is not awaiting review (next={state.next})")
    
    threading.Thread(
        target=_resume_graph,
        args=(config, file_reviews),
        daemon=True,
    ).start()

    return { "status": "resumed" }

async def stream_pipeline(thread_id:str) -> StreamingResponse:
    config = {"configurable": {"thread_id": thread_id}}

    state = graph.get_state(config)
    if not state.values:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    async def event_generator():
        seen_nodes = set()

        while True:
            state = graph.get_state(config)

            for node in state.metadata.get("writes", {}).keys():
                if node not in seen_nodes:
                    seen_nodes.add(node)
                    yield f"data: {json.dumps({'type': 'node_complete', 'node': node})}"

            if state.next and state.next[0] == "review":
                yield f"data: {json.dumps({'type': 'pending_review', 'file_diffs': state.values['file_diffs']})}\n\n"
                break

            # ran to END → emit pr_url and stop
            if not state.next:
                yield f"data: {json.dumps({'type': 'complete', 'pr_url': state.values.get('pr_url')})}\n\n"
                break

            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        event_generator(),
        media_type='text/event-stream',
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

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