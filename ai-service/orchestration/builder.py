from langgraph.graph import END, StateGraph

from orchestration.decision_functions import index_decision, review_decision
from orchestration.nodes import analyze_node, check_index_node, diff_node, generate_node, index_node, plan_node, pr_node, regenerate_node, review_node
from orchestration.state import GraphState

def build_graph(checkpointer):
    graph = StateGraph(GraphState)

    graph.add_node("check_index", check_index_node)
    graph.add_node("index", index_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("plan", plan_node)
    graph.add_node("generate", generate_node)
    graph.add_node("diff", diff_node)
    graph.add_node("review", review_node)
    graph.add_node("regenerate", regenerate_node)
    graph.add_node("pr", pr_node)


    graph.set_entry_point("check_index")
    graph.add_conditional_edges(
        "check_index",
        index_decision,
        {
            "index": "index",
            "skip": "analyze"
        }
    )
    graph.add_edge("index", "analyze")
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "generate")
    graph.add_edge("generate", "diff")
    graph.add_edge("diff", "review")
    graph.add_conditional_edges(
        "review",
        review_decision,
        {
            "approve": "pr",
            "reject": "regenerate"
        }
    )
    graph.add_edge("regenerate", "diff")
    graph.add_edge("pr", END)

    return graph.compile(checkpointer=checkpointer)