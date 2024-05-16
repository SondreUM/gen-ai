from googlesearch import search, SearchResult
from chat import LLM

def parse_results(results: list[SearchResult], query: str, verbose: bool) -> list[str]:
    agent = LLM()
    relevant = []

    agent.invoke(f"""You are an investigator looking for information about a company and it's employees.
                 You are specifically looking for information about the the company called {query}.""")

    for result in results:
        description = result.description

        response = agent.invoke(f"""Do you think it is likely that a page with the following description would contain relevant information about {query}?
                                Include a yes/no in your answer in addition to your reasoning.\n
                                {description}""")
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

    # search for what the query is, and what it does, this is to get more diverse links to crawl
    query_what = f"what is {query}"
    query_do = f"what does {query} do"
    results_what = list(search(query_what, lang='en', advanced=True))
    results_do = list(search(query_do, lang='en', advanced=True))

    results.extend(results_what)
    results.extend(results_do)

    relevant = parse_results(results, query, verbose)

    # remove duplciates, and return relevant urls
    return list(set([relevant.url for relevant in relevant]))
