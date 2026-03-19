from orchestration.state import GraphState

def review_decision(state:GraphState):
    if state.get('approved'):
        return "approve"
    return "reject"

def index_decision(state:GraphState):
    if state.get('is_indexed'):
        return "skip"
    return "index"