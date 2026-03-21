from orchestration.state import GraphState

def review_decision(state:GraphState):
    rejected = [
        f for f in state['file_reviews']
        if not f['approved']
    ]
    
    if not rejected:
        return "approve"
    
    # state['rejected_files'] = rejected
    state['attempt'] = state.get('attempt', 0) + 1

    return 'reject'
    # if state.get('approved'):
    #     return "approve"
    # return "reject"

def index_decision(state:GraphState):
    if state.get('is_indexed'):
        return "skip"
    return "index"