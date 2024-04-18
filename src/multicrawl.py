from scrapy.crawler import CrawlerProcess
from crawler.spiders.quotes_spider import QuotesSpider
from scrapy.utils.project import get_project_settings
import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    max_depth = int(args.pop(0))
    urls = args

    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(QuotesSpider, urls=urls, max_depth=max_depth)
    process.start()