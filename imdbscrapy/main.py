from analysis import ImdbAnalysis
from imdb_spider import *
import logging

logging.basicConfig(filename='logs.log')
logging.getLogger('PIL').setLevel(logging.WARNING)

process = CrawlerProcess()  # instantiates CrawlerProcess, a Scrapy utility to run a spider from a python script
process.crawl(ImdbSpider)   # runs the crawler with the given spider class name
process.start()             # the script will block here until the crawling is finished

imdb_top250 = ImdbAnalysis('IMDBTop250.csv')  # instantiates an analysis with the given output from the crawl
imdb_top250.show_graphs()  # run the method to analyze and show graphical representations of the data
