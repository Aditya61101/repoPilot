from typing import List
from langchain_core.messages import SystemMessage, HumanMessage
from models.patch_generator import PatchSet
from patch_generation.generator_context import extract_dependency_context
from patch_generation.prompts import build_patch_generator_system_prompt, build_patch_generator_user_prompt
from utils.llm_client import set_llm

patch_llm = set_llm(max_tokens=4000).with_structured_output(PatchSet)
SYSTEM_PROMPT = build_patch_generator_system_prompt()

def generate_batch_patches(issue, batch, patch_results, patch_lookup, repo_state):
    requests = []
    for step in batch:
        target_file_content = repo_state[step['file']]
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
        requests.append([
            SystemMessage(SYSTEM_PROMPT),
            HumanMessage(user_prompt)
        ])
    responses:List[PatchSet] = patch_llm.batch(requests)
    return responses
