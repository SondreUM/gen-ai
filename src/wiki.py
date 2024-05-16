import config
from pathlib import Path
from requests import get
from gpt import init_agent
import wikipedia

def parse_results(results: list, query: str, verbose: bool) -> list[str]:
    agent = init_agent()
    
    agent.invoke(f"""You are an investigator looking for information about a company.
                 You are specifically looking for information about the the company called {query}.
                 You need to find the single most relevant wikipedia page about the company given a list of JSON data.
                 Only return the ID of the single most relevant page""")
    
    most_relevant = results[0]
    most_relevant_description = most_relevant["description"]

    results = results[1:]
    if len(results) == 0:
        print("Only 1 search result from wikipedia, returning it.")
        return most_relevant

    # Compare descriptions to find the most relevant page
    for result in results:
        description = result["description"]
        response = agent.invoke(f""" Which of the following descriptions is most likely to contain relevant information about {query}?
                                Descriptipn 1: {most_relevant_description} or description 2: {description}\n
                                Do you think decription 1 is better than description 2?
                                Respond only with yes if decription 1 is better, and no if description 2 is better.\n
                                """).content
        
        if "no" in response.lower()[:5]:
            most_relevant = result
        elif verbose:
            print(f"Discarding {result['key']}")
            print(f"Reasoning: {response}")
            print(f"Description: {description}\n")

    return most_relevant

def search_wikipedia(query: str) -> None:
    """Search wikipedia for the query"""
    parsed_dir: Path = Path(config.DATA_PATH).joinpath("parsed_data")
    modified_query = query.replace(" ", "%20")
    modified_query = modified_query.replace("&", "%26")

    # search for appropriate wikipedia page (limit defines how many results to return)
    response = get(f"https://api.wikimedia.org/core/v1/wikipedia/en/search/title?q={modified_query}&limit=6")
    data = response.json()

    if len(data["pages"]) == 0:
        print("No wikipedia page found, try using a more specific query.")
        return
    
    most_relevant_page = parse_results(data["pages"], query, False)
    id = most_relevant_page["id"]

    # Get page by id
    page = wikipedia.page(pageid=id)

    with open(parsed_dir.joinpath("wikipedia.md"), "w", encoding="utf-8", errors="ignore") as f:
        f.write(page.content)


