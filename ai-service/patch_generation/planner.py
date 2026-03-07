from langchain_core.messages import SystemMessage, HumanMessage
from models.patch_planning import PatchPlan
from patch_generation.prompts import build_patch_planner_system_prompt, build_patch_planner_user_prompt
from utils.llm_client import set_llm

def plan_patch(issue, analysis_text, context):
    system_prompt = build_patch_planner_system_prompt()
    user_prompt = build_patch_planner_user_prompt(issue, analysis_text, context)

    llm = set_llm(max_tokens=800).with_structured_output(PatchPlan)

    response:PatchPlan = llm.invoke([
        SystemMessage(system_prompt),
        HumanMessage(user_prompt)
    ])
    print("patch planner response:", response.model_dump())
    return response.model_dump()