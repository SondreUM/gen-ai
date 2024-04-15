from scrapy.crawler import CrawlerProcess
from crawler.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings

from gpt import init_agent, PROJECT_PATH
import os

if __name__ == "__main__":
    # clean up data directory
    html_files = os.listdir(f"{PROJECT_PATH}/crawler_data")
    for file in html_files:
        os.remove(f"crawler_data/{file}")

    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(QuotesSpider, urls=["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"], max_depth=2)
    process.start()