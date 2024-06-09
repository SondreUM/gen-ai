#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from pathlib import Path
import subprocess
import platform
from parseHTML import parse_HTML_v2
from argument_parser import init_parser
from googling import search_google
from wiki import search_wikipedia
from filter import filter_data

# API imports
from api.bnn.interface import BNN, write2file
from api.yellowpages.yellowpages import YellowpagesAPI

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

    run_crawler(relevant_urls, 0)
    search_wikipedia(org)
    parse_HTML_v2()

    # run API modules
    yellow = YellowpagesAPI()
    # organization number provided
    if args.orgnr:
        orgnum = args.orgnr
        yellow.get(orgnum, org)
        BNN.get_org(orgnum)

    # search for organization number
    else:
        results = yellow.search(args.entity)

        # Get the first 3 results
        first_3 = results[:3]
        for contact in first_3:
            orgnum = contact["organizationNumber"]
            name = contact["name"]
            yellow.get(orgnum, name)

            BNN.get_org(orgnum)

    filter_data(org)
