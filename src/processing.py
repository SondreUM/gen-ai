#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from pathlib import Path
import subprocess
import platform
from requests import get
from html2text import HTML2Text
from api.yellowpages.yellowpages import YellowpagesAPI
from parseHTML import parse_HTML
from argument_parser import init_parser
from googling import search_google
from gpt import init_agent

def run_crawler(urls: list[str], max_depth: int):
    """Bypass limitations of scrapy by running the crawler in a separate process"""
    computer = platform.system()

    match computer:
        case "Windows":
            subprocess.run(
                ["python", config.PROJECT_PATH.joinpath("multicrawl.py")] + [str(max_depth)] + urls
            )
        case "Linux" | "Darwin":
            subprocess.run(
                ["python3", config.PROJECT_PATH.joinpath("multicrawl.py")] + [str(max_depth)] + urls
            )
        case _:
            print("OS not supported")


def use_gpt(data: str, organization: str) -> str:
    """Use the GPT model to filter the data"""
    agent = init_agent()

    response = agent.invoke(f"""You are an investigator looking for information about a company and it's employees.
                            This includes, but is not limited to, contact information, organization number, products, services,
                            and other information that would help give a more complete picture of the company.
                            You are specifically looking for information about the the company called {organization}.
                            Only respond with relevant information. if absolutely no useful information can be extract from the text,
                            respond with 'NOTHING'. If specific information is not present in the text, do not make up information,
                            instead designate the information as 'not found'.
                            Can you efficiently extract the relevant information from the following text:\n
                            {data}""")
    
    return response.content if "NOTHING" not in response.content else ""


def filter_data(organization: str) -> None:
    """Filter parsed data extract relevant information"""
    parsed_dir: Path = Path(config.DATA_PATH).joinpath("parsed_data")
    filtered_dir = parsed_dir.parent.joinpath("filtered_data")
    filtered_dir.mkdir(parents=True, exist_ok=True)
    for file in filtered_dir.iterdir():
        file.unlink()

    for file in parsed_dir.iterdir():
        result = ""
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = ""
            tokens = 0
            # read at least 3000 tokens before invoking the model (model limit of gpt-35 is 4096 tokens)
            while True:
                new_line = f.readline()
                if len(new_line) == 0:
                    # end of file
                    gpt_response = use_gpt(data, organization)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    break
                elif tokens > 3000:
                    # approaching token limit
                    data += new_line
                    gpt_response = use_gpt(data, organization)
                    if len(gpt_response) > 0:
                        result += f"\n{gpt_response}"
                    data = ""
                    tokens = 0
                else:
                    # continue reading
                    data += new_line
                    tokens += len(new_line.split())

        # write the filtered data to a new file
        if len(result) > 0:
            with open(f"{filtered_dir.joinpath(file.name)}", "w", encoding="utf-8", errors="ignore") as f:
                f.write(result)


def remove_duplicates() -> None:
    """Remove duplicate information from the filtered data"""
    filtered_dir: Path = Path(config.DATA_PATH).joinpath("filtered_data")

    for file in filtered_dir.iterdir():
        duplicate_free = ""
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            # remove duplicates
            agent = init_agent()
            response = agent.invoke(f"""return the same exact information back to me after removing duplicate information within the data:\n
                                    {data}""")
            duplicate_free = response.content
        with open(f"{filtered_dir.joinpath(file.name)}", "w", encoding="utf-8", errors="ignore") as f:
            f.write(duplicate_free)
            

def search_wikipedia(query: str) -> None:
    """Search wikipedia for the query"""
    crawler_dir: Path = Path(config.DATA_PATH).joinpath("crawler_data")
    modified_query = query.replace(" ", "%20")
    modified_query = modified_query.replace("&", "%26")

    # search for appropriate wikipedia page (limit defines how many results to return)
    response = get(f"https://api.wikimedia.org/core/v1/wikipedia/en/search/title?q={modified_query}&limit=1")
    data = response.json()
    id = data["pages"][0]["id"]

    # fetch the page
    response = get(f"http://en.wikipedia.org/?curid={id}")
    data = response.text

    with open(crawler_dir.joinpath("wikipedia.html"), "w", encoding="utf-8", errors="ignore") as f:
        f.write(data)
            

if __name__ == "__main__":
    config.init_paths()
    arg_parser = init_parser()
    args = arg_parser.parse_args()
    org = args.entity

    # clean up data directory
    path: Path = config.DATA_PATH.joinpath("crawler_data")
    path.mkdir(parents=True, exist_ok=True)
    for file in path.iterdir():
        file.unlink()
    
    relevant_urls = search_google(org)

    # remove wikipedia links due to their extreme amounts of links
    # wikipedia search is handled separately
    to_remove = []
    for url in relevant_urls:
        if "wikipedia" in url.lower():
            to_remove.append(url)
    for url in to_remove:
        relevant_urls.remove(url)

    run_crawler(relevant_urls, 1)
    search_wikipedia(org)
    parse_HTML()
    filter_data(org)
    # remove_duplicates()

    # yellow = YellowpagesAPI()
    # results = yellow.search("uit")

    # # Get the first 3 results
    # first_3 = results[:3]
    # for contact in first_3:
    #     orgnum = contact['organizationNumber']
    #     name = contact['name']
    #     yellow.get(orgnum, name)
