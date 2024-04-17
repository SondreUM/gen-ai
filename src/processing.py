#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from scrapy.crawler import CrawlerProcess
from crawler.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings

from gpt import init_agent, PROJECT_PATH
import os

if __name__ == "__main__":
    # clean up data directory
    path: Path = Path(PROJECT_PATH).joinpath("crawler_data")

    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(
        QuotesSpider,
        urls=["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"],
        max_depth=2,
    )
    process.start()
