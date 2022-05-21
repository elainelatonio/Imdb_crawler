import scrapy
from items import Imdb_item
import re
import logging
from scrapy.crawler import CrawlerProcess

class ImdbSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']  # sets the allowed domain to crawl
    start_urls = ['http://www.imdb.com/chart/top']  # sets initial url to crawl

    # specifies where to export the data, file type/format and method
    custom_settings = {'FEEDS': {'IMDBTop250.csv': {"format": 'csv', 'overwrite': True}}}

    def __init__(self):
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)  # customized logging level to reduce noise
        super().__init__()

    # scrapy's default implementation generates Request(url, dont_filter=True) for each url in start_urls, which
    # produces the response we pass into the parse method below
    # parse method first gets movie details present in the Top 250 page and places them in a list
    def parse(self, response):
        number = 0
        titles = response.css("td.titleColumn a::text").getall()
        movie_ids = response.css("td.watchlistColumn div::attr(data-tconst)").getall()
        years = response.css("td.titleColumn span::text").getall()
        ratings = response.css("td.posterColumn span[name=ir]::attr(data-value)").getall()
        votes = response.css("td.posterColumn span[name=nv]::attr(data-value)").getall()
        ranks = response.css("td.posterColumn span[name=rk]::attr(data-value)").getall()

        # iterate through each movie url (there should be 250)
        for href in response.css("td.titleColumn a::attr(href)").getall():
            item = Imdb_item()  # create an item with fields defined in the items module. each item is a movie
            item['title'] = titles[number]  # set the value of the field of this item to be the nth element in the list
            item['movie_id'] = movie_ids[number]
            item['year'] = years[number][1:5]
            item['rating'] = ratings[number]
            item['votes'] = votes[number]
            item['rank'] = ranks[number]
            number += 1
            # create a new request to crawl the movie url, pass the item (movie) into the callback function parse_movie
            request = scrapy.Request(response.urljoin(href), callback=self.parse_movie, cb_kwargs=dict(movie=item))
            yield request

    # this parses the data from each movie url
    # fields of the movie item not filled from the Top 250 page crawl will be populated here using xpaths
    def parse_movie(self, response, movie):
        movie['movie_link'] = response.url
        movie['genre'] = response.xpath("//li[@data-testid='storyline-genres']/div/ul/li/a/text()").getall()
        movie['runtime_mins'] = (int(response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").
            getall()[0]) * 60 if 'hours' in response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").
            getall() else 0) + (int(re.findall('(\d+) minutes', ''.join(map(str, response.xpath
            ("//li[@data-testid='title-techspec_runtime']/div/text()").getall())))[0]) if 'minutes' in response.xpath(
            "//li[@data-testid='title-techspec_runtime']/div/text()").getall() else 0)
        movie['origin'] = response.xpath("//li[@data-testid='title-details-origin']/div/ul/li/a/text()").getall()
        movie['awards_wins'] = ''.join(map(str, (re.findall('(\d+) wins', response.xpath(
            "//li[@data-testid='award_information']/div/ul/li/span/text()").getall()[0], re.IGNORECASE))))
        movie['awards_nominations'] = ''.join(map(str, (re.findall('(\d+) nominations', response.xpath(
            "//li[@data-testid='award_information']/div/ul/li/span/text()").getall()[0], re.IGNORECASE))))
        movie['gross_worldwide_usd'] = response.xpath(
            "//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div/ul/li/span/text()").get().replace('$','') \
            if response.xpath("//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div/ul/li/span/text()").\
                   get() is not None else 0
        return movie

# to run the crawler script as a standalone python file (i.e., not from main.py)
if __name__ == "__main__":
    process = CrawlerProcess()  # instantiates CrawlerProcess, a Scrapy utility to run a spider from a python script
    process.crawl(ImdbSpider)  # runs the crawler with the given spider name defined in imdb_spider.py
    process.start()  # the script will block here until the crawling is finished
