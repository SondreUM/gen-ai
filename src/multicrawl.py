#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from scrapy.crawler import CrawlerProcess
from crawler.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings
import multiprocessing as mp
from numpy import array_split


def multicrawl(link_depth: tuple[list[str], int], timeout: int = 900) -> None:
    """Crawl the urls to a specified depth"""
    urls, max_depth = link_depth
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(QuotesSpider, urls=urls, max_depth=max_depth)
    process.start()
    print(f"Finished crawling {urls} to a depth of {max_depth}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 multicrawl.py <max_depth> <url1> <url2> ...")
        sys.exit(1)

    max_depth = int(sys.argv[1])
    urls: list[str] = sys.argv[2:]

    # divide up urls and crawl them in parallel/concurrently
    splits = array_split(urls, mp.cpu_count())
    splits = [split.tolist() for split in splits if split.size > 0]
    input = [(split, max_depth) for split in splits]
    
    with mp.Pool() as pool:
        for result in pool.imap_unordered(multicrawl, input):
            pass