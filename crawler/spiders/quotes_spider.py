from pathlib import Path
from typing import Any
import scrapy
from scrapy.crawler import CrawlerProcess

ROOT_PATH = Path(__file__).parent.parent.parent
DATA_PATH = ROOT_PATH / "crawler_data"

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        "https://machine-learning.uit.no/",
    ]

    # allow injection of urls to scrape
    def __init__(self, name: str | None = None, urls: list[str] = [], **kwargs: Any):
        if type(urls) == list[str]:
            if len(urls) > 0:
                self.start_urls = urls
        super().__init__(name, **kwargs)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"

        # check that the data directory exists
        if not DATA_PATH.exists():
            DATA_PATH.mkdir()
        
        # save data
        (DATA_PATH / filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider, urls=["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"])
    process.start()