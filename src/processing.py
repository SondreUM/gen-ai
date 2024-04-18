#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from gpt import PROJECT_PATH
import subprocess
import platform


def run_crawler(urls: list[str], max_depth: int):
    """Bypass limitations of scrapy by running the crawler in a separate process"""
    computer = platform.system()

    match computer:
        case "Windows":
            subprocess.run(
                ["python", PROJECT_PATH.joinpath("multicrawl.py")] + [str(max_depth)] + urls
            )
        case "Linux", "Darwin":
            subprocess.run(
                ["python3", PROJECT_PATH.joinpath("multicrawl.py")] + [str(max_depth)] + urls
            )
        case _:
            print("OS not supported")


if __name__ == "__main__":
    # clean up data directory
    path: Path = Path(PROJECT_PATH).joinpath("crawler_data")

    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    run_crawler(["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"], 2)
    run_crawler(["https://uit.no/startsida"], 1)
