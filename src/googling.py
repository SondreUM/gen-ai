from googlesearch import search, SearchResult
from gpt import init_agent

def parse_results(results: list[SearchResult], query: str, verbose: bool) -> list[str]:
    agent = init_agent()
    relevant = []

    agent.invoke(f"""You are an investigator looking for information about a company and it's employees.
                 You are specifically looking for information about the the company called {query}.""")

    for result in results:
        description = result.description

        response = agent.invoke(f"""Do you think it is likely that a page with the following description would contain relevant information about {query}?
                                Include a yes/no in your answer in addition to your reasoning.\n
                                {description}""").content
        if "yes" in response.lower():
            relevant.append(result)
        elif verbose:
            print(f"Discarding {result.url}")
            print(f"Reasoning: {response}")
            print(f"Description: {description}\n")
    if verbose:
        print("\nRelevant results:")    
        for result in relevant:
            print(f"{result}\n")

    return relevant


def search_google(query: str, verbose = False) -> list[str]:
    """Search google for the query, and return relevant ones"""
    results = list(search(query, lang='en', advanced=True))

    relevant = parse_results(results, query, verbose)

    # remove duplciates, and return relevant urls
    return list(set([relevant.url for relevant in relevant]))