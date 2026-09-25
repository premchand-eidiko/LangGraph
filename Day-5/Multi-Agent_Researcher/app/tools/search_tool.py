from langchain_tavily import TavilySearch


search = TavilySearch(
    max_results=5,
)


def search_web(query: str) -> str:
    result = search.invoke(
        {
            "query": query
        }
    )

    return str(result)