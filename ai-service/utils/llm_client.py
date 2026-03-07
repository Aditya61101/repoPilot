import os
from langchain_openai.chat_models import AzureChatOpenAI

def set_llm(max_tokens=2048, temperature=0):
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv('AZURE_OPENAI_GPT_4O_DEPLOYMENT'),
        api_version=os.getenv('AZURE_OPENAI_GPT_4O_VERSION'),
        api_key=os.getenv('AZURE_OPENAI_GPT_4O_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_GPT_4O_ENDPOINT'),
        max_tokens=max_tokens,
        temperature=temperature
    )
    return llm