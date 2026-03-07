from langchain_core.messages import SystemMessage, HumanMessage
from llm.prompts import build_analysis_system_prompt, build_analysis_user_prompt
from llm.client import set_llm
from models.analysis_result import AnalysisResult

def analyze_issue(issue, code_context):
    system_prompt = build_analysis_system_prompt()
    user_prompt = build_analysis_user_prompt(issue=issue, code_context=code_context)

    llm = set_llm(max_tokens=800).with_structured_output(AnalysisResult)

    response:AnalysisResult = llm.invoke(
        [SystemMessage(
            system_prompt
        ),
        HumanMessage(
            user_prompt
        )]
    )
    print("analyzer response:", response.model_dump())
    return response.model_dump()