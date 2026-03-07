def build_analysis_system_prompt():
    return """
    You are a senior software engineer analyzing a GitHub issue.

    Your task:
    1. Identify the root cause in the provided code.
    2. Reference specific functions or logic responsible.
    3. Determine which files should be edited.

    Focus on concrete implementation details, not generic explanations.

    Return ONLY valid JSON in this format:

    {
    "root_cause": "short explanation",
    "relevant_files": [
        {
        "file": "path/to/file",
        "reason": "why it is relevant"
        }
    ],
    "functions_involved": ["function1", "function2"],
    "suggested_edit_files": ["path/to/file"]
    }

    Do not include anything outside JSON.
"""

def build_analysis_user_prompt(issue, code_context):
    return f"""
    ### ISSUE:
    {issue}
    ### CODE CONTEXT:
    {code_context}
    """