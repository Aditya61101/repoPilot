def format_analysis(analysis: dict) -> str:

    root_cause = analysis.get("root_cause", "")
    relevant_files = analysis.get("relevant_files", [])
    functions = analysis.get("functions_involved", [])
    suggested = analysis.get("suggested_edit_files", [])

    # format relevant files with reasons
    relevant_text = []
    for item in relevant_files:
        file = item.get("file", "")
        reason = item.get("reason", "")
        relevant_text.append(f"- {file}\n  Reason: {reason}")

    # format functions
    functions_text = "\n".join(f"- {f}" for f in functions)

    # format suggested files
    suggested_text = "\n".join(f"- {f}" for f in suggested)

    text = f"""
ROOT CAUSE
----------
{root_cause}

FUNCTIONS INVOLVED
------------------
{functions_text}

RELEVANT FILES
--------------
{chr(10).join(relevant_text)}

SUGGESTED EDIT FILES
--------------------
{suggested_text}
"""

    return text.strip()