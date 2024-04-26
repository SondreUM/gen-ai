#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from pathlib import Path
import subprocess
import platform
from api.yellowpages.yellowpages import YellowpagesAPI
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.docstore.document import Document


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

    crawler_dir: Path = Path(config.DATA_PATH).joinpath("crawler_data")
    parsed_dir = crawler_dir.parent.joinpath("parsed_data")
    parsed_dir.mkdir(parents=True, exist_ok=True)

    for file in parsed_dir.iterdir():
        file.unlink()

    bs4_transformer = BeautifulSoupTransformer()
    exclude = ["style", "script", "head", "title", "meta", "[document]"]
    include = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li", "div", "span"]
    document = []
 
    for file in crawler_dir.iterdir():
        if file.is_dir():
            continue

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            doc =  Document(page_content=data, metadata={"source": "local"})
            document.append(doc)

    docs_transformed = bs4_transformer.transform_documents(document, unwanted_tags=exclude, tags_to_extract=include, remove_comments=True, remove_lines=False)

    for idx, file in enumerate(crawler_dir.iterdir()):
        if file.is_dir():
            continue
        
        with open(f"{parsed_dir.joinpath(file.with_suffix('.md').name)}", "w", encoding="utf-8", errors="ignore") as f:
            f.write(docs_transformed[idx].page_content)


if __name__ == "__main__":
    config.init_paths()
    # clean up data directory
    path: Path = config.DATA_PATH.joinpath("crawler_data")
    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    run_crawler(["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"], 2)
    run_crawler(["https://uit.no/startsida"], 1)

    parse_data()


    # yellow = YellowpagesAPI()
    # results = yellow.search("uit")

    # # Get the first 3 results
    # first_3 = results[:3]
    # for contact in first_3:
    #     orgnum = contact['organizationNumber']
    #     name = contact['name']
    #     yellow.get(orgnum, name)