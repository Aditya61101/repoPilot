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
You are a senior software engineer responsible for implementing precise code patches.

Your job is to implement the patch plan using the provided code context.

Rules:
1. Only modify the code required by the edit strategy.
2. Do not rewrite unrelated parts of the file.
3. Preserve existing coding style and libraries.
4. Do not invent files, functions, or APIs not present in the context.
5. Keep patches minimal and localized.
6. Most patch-plan steps should produce a single patch unless multiple edits are required as per edit_strategy.
"""

def build_patch_generator_user_prompt(issue, step, target_file_content, dependency_context):
    step_str = json.dumps(step, indent=2)
    # start_line = step['start_line']
    # end_line = step['end_line']
    # symbol = step.get('symbol', '')
    # edit_strategy = step['edit_strategy']
    # main_symbol_to_focus = f"Main Symbol to focus on: {symbol}" if symbol else ''
    
    return f"""
Issue
{issue}

Patch Plan Step
{step_str}

IMPORTANT:
Modify ONLY the code within the specified patch region. Do changes in other part of file_content only when required like adding extra import of dependencies etc.
Do not rewrite the entire file.

Full Target file for context:
{target_file_content}

Dependency patch results
The following upstream patches were already applied.
Your patch must remain compatible with these changes.
{dependency_context}

Task:
Implement the modification described in the edit_strategy.
Don't include explanations, follow the output schema.
"""

# def build_semantic_scheduler_system_prompt():
#     return """
# You are a software architecture expert.

# Follow these rules:
# 1. Modify only the specified file.
# 2. Respect start_line and end_line.
# 3. Ensure compatibility with dependency patches.
# 4. Preserve surrounding code style.
# 5. Do not modify unrelated code.

# Return only the structured PatchSet.
# """