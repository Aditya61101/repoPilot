def build_planner_query(issue:str, analysis_json:dict) -> str:
    root_cause = analysis_json.get('root_cause', '')
    functions = ", ".join(analysis_json.get('functions_involved', []))
    files = ", ".join(analysis_json.get('suggested_edit_files', []))

    return f"""
    Issue:
    {issue}
    
    Root cause:
    {root_cause}

    Functions involved:
    {functions}

    Suggested edit files:
    {files}
    """.strip()
    