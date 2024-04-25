#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from pathlib import Path
import subprocess
import platform
from api.yellowpages.yellowpages import get_yellowpages_data
import html2text
from argument_parser import init_parser
from googling import search_google

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

def parse_data():
    """Parse the data collected by the crawler"""
    crawler_dir: Path = Path(config.PROJECT_PATH).joinpath("crawler_data")
    parsed_dir = crawler_dir.joinpath("parsed")
    parsed_dir.mkdir(parents=True, exist_ok=True)
    for file in parsed_dir.iterdir():
        file.unlink()

    h = html2text.HTML2Text()

    for file in crawler_dir.iterdir():
        if file.is_dir():
            continue
        parsed_data = None
        with open(file, "r") as f:
            data = f.read()
            parsed_data = h.handle(data)
        with open(f"{parsed_dir.joinpath(file.with_suffix('.md').name)}", "w") as f:
            f.write(parsed_data)


def search_wikipedia(query: str) -> None:
    """Search wikipedia for the query"""
    pass
            

if __name__ == "__main__":
    config.init_paths()
    # clean up data directory
    path: Path = config.DATA_PATH.joinpath("crawler_data")
    path.mkdir(parents=True, exist_ok=True)
    for file in path.iterdir():
        file.unlink()
    arg_parser = init_parser()
    args = arg_parser.parse_args()
    org = args.entity
    relevant_urls = search_google(org)

    # remove wikipedia links due to their extreme amounts of links
    for i in range(len(relevant_urls)):
        if "wikipedia" in relevant_urls[i]:
            relevant_urls.pop(i)
            break

    run_crawler(relevant_urls, 2)
    parse_data()
