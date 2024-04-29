#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from pathlib import Path
import subprocess
import platform
from api.yellowpages.yellowpages import YellowpagesAPI
from parseHTML import parse_HTML


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
    # clean up data directory
    path: Path = config.DATA_PATH.joinpath("crawler_data")
    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    run_crawler(["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"], 2)
    run_crawler(["https://uit.no/startsida"], 1)

    parse_HTML()


    # yellow = YellowpagesAPI()
    # results = yellow.search("uit")

    # # Get the first 3 results
    # first_3 = results[:3]
    # for contact in first_3:
    #     orgnum = contact['organizationNumber']
    #     name = contact['name']
    #     yellow.get(orgnum, name)