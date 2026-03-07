def format_analysis(analysis:dict) -> str:
    a = analysis.get('analysis',  {})

    root_cause = a.get("root_cause", "")
    relevant_files = a.get("relevant_files", [])
    functions = a.get("functions_involved", [])
    suggested = a.get("suggested_edit_files", [])

    text = f"""
    ROOT CAUSE
    ----------
    {root_cause}

    RELEVANT FILES
    ---------------
    {", ".join(relevant_files)}

    FUNCTIONS INVOLVED
    ------------------
    {", ".join(functions)}

    SUGGESTED EDIT FILES
    --------------------
    {", ".join(suggested)}
    """
    return text.strip()