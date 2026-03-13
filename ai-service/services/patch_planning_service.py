import pprint
from rag.retriever import retrieve
from rag.context_builder import build_llm_context
from utils.analysis_formatter import format_analysis
from utils.planner_query_builder import build_planner_query
from patch_generation.planner import plan_patch

def patch_planning(repo_key, issue, analysis_json):

    planner_query = build_planner_query(issue, analysis_json)
    print(f'planner query: {planner_query}')

    grouped_chunks = retrieve(repo_key, planner_query, 'plan')
    # return grouped_chunks
    # print("grouped_chunks:")
    # pprint.pprint(grouped_chunks, indent=3)
    
    context = build_llm_context(grouped_chunks)
    analysis_text = format_analysis(analysis_json)
    # return analysis_text
    # # print(f"analysis text: {analysis_text}")
    # # sending to patch planner
    patch_plan = plan_patch(
        issue=issue, 
        context=context,
        analysis_text=analysis_text
    )

    return patch_plan