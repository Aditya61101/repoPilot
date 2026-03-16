import os
from tavily import TavilyClient
from langchain.tools import tool

client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool
def search_web(query:str) -> str:
    """
    Search the web for programming documentation or code examples.
    Useful for external APIs, libraries, frameworks or patterns.
    """

    print(f"[SEARCH QUERY] {query}")
    result = client.search(
        query=query,
        search_depth='advanced',
        max_results=3
    )

    snippets = []
    for r in result['results']:
        print("TITLE:", r.get("title"))
        print("URL:", r.get("url"))
        print("CONTENT:", r.get("content")[:5000])
        print("-" * 60)
        snippets.append(
            f"""
            Title: {r['title']}

            Snippet:
            {r['content'][:5000]}

            URL: {r['url']}
            """
        )

    return "\n".join(snippets)