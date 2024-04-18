#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from scrapy.crawler import CrawlerProcess
from crawler.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings


def multicrawl(max_depth: int, urls: list[str] | tuple[str], timeout: int = 900) -> None:

    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(QuotesSpider, urls=urls, max_depth=max_depth)
    process.start()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 multicrawl.py <max_depth> <url1> <url2> ...")
        sys.exit(1)

    max_depth = int(sys.argv[1])
    urls: list[str] = sys.argv[2:]

    multicrawl(max_depth, urls)
