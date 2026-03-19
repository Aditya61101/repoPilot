import uuid
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

    result = None
    for event in graph.stream(
        initial_state,
        config=config,
        interrupt_before=['review']
    ):
        for node_name, node_output in event.items():
            print(f"[NODE NAME] -> {node_name}")
            if node_name == '__interrupt__':
                break
            result = node_output

    return  {
        "thread_id": thread_id,
        "diff": result['diff']
    }

def review_pipeline(thread_id, approved, feedback=None):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    resume_state = {
        "approved": approved,
        "feedback": feedback
    }
    graph.update_state(
        config,
        resume_state
    )
    result = None
    for event in graph.stream(
        None,
        config=config
    ):
        for node_name, node_output in event.items():
            print(f"[PIPELINE] -> {node_name}")
            if node_name == '__interrupt__':
                break
            result = node_output

    return {
        "pr_url": result['pr_url']
    }