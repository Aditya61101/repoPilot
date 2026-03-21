# from typing import List
from langchain_core.messages import SystemMessage, HumanMessage
# from models.patch_generator import PatchSet
from models.patch_generator import GeneratedSymbol
from patch_generation.generator.generator_context import extract_dependency_context
from patch_generation.prompts import build_patch_generator_system_prompt, build_patch_generator_user_prompt
# from tools.tool_registry import TOOLS
from utils.llm_client import set_llm
# from concurrent.futures import ThreadPoolExecutor

# generator_llm = (set_llm(max_tokens=4000).bind_tools(TOOLS))
generator_llm = set_llm(max_tokens=4000).with_structured_output(GeneratedSymbol)
SYSTEM_PROMPT = build_patch_generator_system_prompt()
# tool_map = {tool.name: tool for tool in TOOLS}

# def generate_patch_step(user_prompt):
#     messages = [
#         SystemMessage(SYSTEM_PROMPT),
#         HumanMessage(user_prompt)
#     ]

#     while True:
#         response = generator_llm.invoke(messages)
#         if not response.tool_calls:
#             print("[NO TOOL USED]")
#         elif response.tool_calls:
#             print("\n[TOOL CALL DETECTED]")
#             print(response.tool_calls)
#             for call in response.tool_calls:
#                 tool = tool_map[call['name']]
#                 result = tool.invoke(call['args'])

#                 messages.append(response)
#                 messages.append({
#                     'role': 'tool',
#                     'tool_call_id': call['id'],
#                     'content': result
#                 })
#             continue
#         break
    
#     structured_llm = generator_llm.with_structured_output(PatchSet)
#     return structured_llm.invoke(messages)

def generate_batch_patches(
    issue, 
    batch, 
    patch_lookup, 
    repo_state,
    feedback_map=None
):
    messages = []
    for step in batch:
        target_file_content = "\n".join(repo_state[step['file']])
        
        feedback = None
        if feedback_map:
            feedback = feedback_map.get(step['file'])
        
        # print("target file content: ", target_file_content)
        dependency_context = extract_dependency_context(
            step=step, 
            patch_lookup=patch_lookup,
            repo_state=repo_state
            # patch_results=patch_results
        )
        user_prompt = build_patch_generator_user_prompt(
            issue, 
            step, 
            target_file_content, 
            dependency_context,
            feedback
        )
        messages.append([
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(user_prompt)
        ])
    responses = generator_llm.batch(messages)
    return responses
