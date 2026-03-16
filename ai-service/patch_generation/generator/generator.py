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

def generate_batch_patches(issue, batch, patch_results, patch_lookup, repo_state):
    # print("system prompt:", SYSTEM_PROMPT)
    # results = []
    # def run_step(step):
    #     target_file_content = repo_state[step['file']]
    #     dependency_context = extract_dependency_context(
    #         step=step, 
    #         patch_lookup=patch_lookup,patch_results=patch_results
    #     )
    #     user_prompt = build_patch_generator_user_prompt(
    #         issue, 
    #         step, 
    #         target_file_content, 
    #         dependency_context
    #     )
    #     return generate_patch_step(user_prompt=user_prompt)
    
    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     futures = [executor.submit(run_step, step) for step in batch]

    #     for f in futures:
    #         results.append(f.result())
    # return results


    # requests = []
    # for step in batch:
    #     requests.append([
    #         SystemMessage(SYSTEM_PROMPT),
    #         HumanMessage(user_prompt)
    #     ])
    # responses:List[PatchSet] = generator_llm.batch(requests)
    # return responses

    messages = []
    for step in batch:
        target_file_content = "\n".join(repo_state[step['file']])
        # print("target file content: ", target_file_content)
        dependency_context = extract_dependency_context(
            step=step, 
            patch_lookup=patch_lookup,patch_results=patch_results
        )
        user_prompt = build_patch_generator_user_prompt(
            issue, 
            step, 
            target_file_content, 
            dependency_context
        )
        messages.append([
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(user_prompt)
        ])
    responses = generator_llm.batch(messages)
    return responses
