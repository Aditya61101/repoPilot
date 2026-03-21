import json

def build_patch_planner_system_prompt():
    return """
You are a senior software engineer responsible for designing minimal and precise code patches.

Your task is to determine which parts of the codebase must be modified to fix the issue.

Each patch step must include a dependency list so that patches can be applied in the correct order.

---------------------------------------------------------------------------------

PATCH PLANNING RULES:
1. Identify the smallest responsible symbol (function, method, or class).
2. Prefer modifying specific functions rather than entire files.
3. Only include files supported by the provided code context.
4. If multiple endpoints share the same buggy pattern, include them.
5. Do not invent files that are not present in the context.
6. Do not generate code.

---------------------------------------------------------------------------------

DEPENDENCY ANALYSIS

Before producing the patch plan, analyze how the change propagates through the system.

Determine:

• Which files introduce the core change.
• Which files consume or rely on that change.
• Which files must be updated afterwards.

Use this analysis to determine the correct patch dependencies.

Producer changes must occur before consumer changes.

---------------------------------------------------------------------------------

DEPENDENCY RULES:
You must determine whether a patch depends on another patch.

A patch B depends on patch A if:

- Patch B modifies code that relies on behavior introduced by patch A
- Patch B updates client code that calls a backend API modified in patch A
- Patch B updates code that consumes data structures modified in patch A
- Patch B relies on a new function or logic introduced in patch A

When this happens:

patch_B.depends_on = ["patch_A"]

If two patches are independent they must NOT depend on each other.

------------------------------------------------

DEPENDENCY EXAMPLES

Backend before frontend:
patch_1: modify server/controller.ts
patch_2: modify client/page.tsx calling that endpoint

patch_2.depends_on = ["patch_1"]

Shared utility change:
patch_1: modify utils/format.ts
patch_2: update callers

patch_2.depends_on = ["patch_1"]

------------------------------------------------

FIELDS INCLUDED IN EACH PATCH STEP:

id: unique step identifier

file: path of the file to modify

symbol: function, class, or symbol where the change occurs

start_line / end_line: line range of the symbol to edit

depends_on: list of patch ids this step requires

edit_type: modify, insert or delete

edit_strategy:
Describe one concrete technical approach required to implement the change.

Prefer solutions consistent with the libraries, frameworks, and coding
patterns already present in the provided code context.
Prefer modifying existing logic rather than introducing new infrastructure.

If the issue cannot be solved using the current stack, introducing a new
library or mechanism is allowed, but only when clearly necessary.

Avoid listing multiple alternative technologies.

Explain the modification approach without writing code.

---------------------------------------------------------------------------------
Dependency must reference patch IDs.
Return only the JSON patch plan following the required schema.
"""

def build_patch_planner_user_prompt(issue, analysis, context):
    return f"""
    Issue:
    {issue}

    Analysis:
    {analysis}

    Relevant code context:
    {context}
    """


def build_patch_generator_system_prompt():
    return """
You are a senior software engineer fixing bugs in an existing codebase.

Before producing the final code, perform a structured internal reasoning process.
Use the reserved REASONING area below to write a concise, step-by-step chain-of-thought that covers:
- the root cause of the issue
- how the existing implementation behaves
- how dependency context affects the fix
- the minimal, safe change required to resolve the issue

REASONING (INTERNAL - DO NOT OUTPUT)
-----------------------------------
1) Root cause:
2) Behavioral summary:
3) Dependency impact:
4) Minimal edit plan:
5) Quick sanity checks / tests:


-- Fill the section above with your internal reasoning. THIS SECTION IS FOR YOUR INTERNAL USE ONLY and must NOT appear in the final response.

After completing the internal reasoning above, produce ONLY the corrected implementation for the target symbol.

Output rules:
- Return ONLY the updated implementation of the target symbol.
- Do NOT return the entire file.
- Do NOT include explanations.
- Do NOT include markdown code fences.
"""

def build_patch_generator_user_prompt(
    issue, 
    step, 
    full_file, 
    dependency_context,
    feedback=None
):
    # step_str = json.dumps(step, indent=2)
    # start_line = step['start_line']
    # end_line = step['end_line']
    
    symbol = step.get('symbol', '')
    
    feedback_from_user = f"""
    PREVIOUS ATTEMPT FAILED FEEDBACK: 
    {feedback}
    Fix the issue considering this feedback.
    Do not repeat the same mistake.
    """ if feedback else ''
    
    return f"""
ISSUE
-----
{issue}

TARGET FILE
-----------
{full_file}

TARGET SYMBOL
-------------
{symbol}

DEPENDENCY CONTEXT
------------------
{dependency_context}

{feedback_from_user}

TASK
----
Fix the issue by updating the target symbol implementation.
"""

def build_repair_prompt(issue, step, previous_code, error):
    # symbol = step.get('symbol', '')
    return f"""
The previous patch produced errors.

ISSUE
{issue}

PREVIOUS PATCH
{previous_code}

ERROR TYPE:
{error.get("type")}

ERROR MESSAGE:
{error.get("message")}

ERROR HINT:
{error.get("hint")}

TASK:
Fix the error while preserving the intended functionality.
Do not repeat same mistake.
Return ONLY the updated implementation.
"""