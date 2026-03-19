from rag.retriever import retrieve
from rag.context_builder import build_llm_context
from patch_generation.planner.analysis_formatter import format_analysis
from patch_generation.planner.planner_query_builder import build_planner_query
from patch_generation.planner.planner import plan_patch

def patch_planning(repo_key, issue, analysis_json, commit_sha):

    planner_query = build_planner_query(issue, analysis_json)

    grouped_chunks = retrieve(repo_key, planner_query, 'plan', commit_sha)
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