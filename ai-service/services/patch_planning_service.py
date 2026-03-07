from rag.retriever import retrieve
from rag.context_builder import build_llm_context
from utils.analysis_formatter import format_analysis
from utils.planner_query_builder import build_planner_query
from patch_generation.planner import plan_patch

def patch_planning(repo_key, issue, analysis_json):

    planner_query = build_planner_query(issue, analysis_json)
    grouped_chunks = retrieve(repo_key, planner_query, 'plan')
    # return grouped_chunks
    context = build_llm_context(grouped_chunks)
    
    analysis_text = format_analysis(analysis_json)

    # sending to patch planner
    patch_plan = plan_patch(
        issue=issue, 
        context=context,
        analysis_text=analysis_text
    )

    return patch_plan