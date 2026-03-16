from rag.retriever import retrieve
from rag.context_builder import build_llm_context
from analysis.analyzer import analyze_issue

def run_issue_analysis(repo_key, issue):
    grouped_chunks = retrieve(repo_key, issue, 'analysis')
    # return grouped_chunks
    context = build_llm_context(grouped_chunks)
    # # return context
    analysis = analyze_issue(issue, context)

    return analysis