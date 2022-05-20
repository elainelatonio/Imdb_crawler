from analysis import ImdbAnalysis
from spiders.imdb_spider import ImdbSpider
from scrapy.crawler import CrawlerProcess
import logging

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)

process = CrawlerProcess()
process.crawl(ImdbSpider)
process.start()

imdb_top250 = ImdbAnalysis()
imdb_top250.show_graphs()
