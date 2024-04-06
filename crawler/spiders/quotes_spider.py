from pathlib import Path
from typing import Any
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import os

ROOT_PATH = Path(__file__).parent.parent.parent
DATA_PATH = ROOT_PATH / "crawler_data"

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = []
    visited = []
    max_depth = 2

    # allow injection of starting urls
    def __init__(self, name: str | None = None, urls: list[str] = [], max_depth: int | None = None, **kwargs: Any):
        self.start_urls = urls
        if max_depth:
            self.max_depth = max_depth

        # check that the data directory exists
        if not DATA_PATH.exists():
            DATA_PATH.mkdir()

        super().__init__(name, **kwargs)

    # find all unvisited links on the page
    def find_links(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))

        return [link for link in links if str(link)[0] == "/" and link not in self.visited]

    def parse(self, response, depth=0):
        self.visited.append(response.url)
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        
        # save data
        (DATA_PATH / filename).write_bytes(response.body)

        if depth >= self.max_depth:
            # limit the depth of the crawler
            return
        
        links = self.find_links(response)
        yield from response.follow_all(links, callback=self.parse, cb_kwargs={"depth": depth + 1})
        # self.log(f"Saved file {filename}")

if __name__ == "__main__":
    # clean up data directory
    html_files = os.listdir(f"{DATA_PATH}")
    for file in html_files:
        os.remove(f"crawler_data/{file}")

    process = CrawlerProcess()
    process.crawl(QuotesSpider, urls=["https://uit.no/research/csg?p_document_id=837262&Baseurl=%2Fresearch%2F"])
    process.start()