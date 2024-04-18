#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from gpt import init_agent, PROJECT_PATH
import subprocess
import platform

def run_crawler(urls: list[str], max_depth: int):
    """Bypass limitations of scrapy by running the crawler in a separate process"""
    computer = platform.system()
    if computer == "Windows":
        print("Windows")
        subprocess.run(["python", f"{PROJECT_PATH}/multicrawl.py"] + [str(max_depth)] + urls)
    elif computer == "Linux" or computer == "Darwin":
        print("Unix")
        subprocess.run(["python3", f"{PROJECT_PATH}/multicrawl.py"] + [str(max_depth)] + urls)
    else:
        print("OS not supported")

if __name__ == "__main__":
    # clean up data directory
    path: Path = Path(PROJECT_PATH).joinpath("crawler_data")

    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    run_crawler(["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"], 2)
    run_crawler(["https://uit.no/startsida"], 1)
