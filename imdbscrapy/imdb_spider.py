import scrapy
from items import Imdb_item
from scrapy.crawler import CrawlerProcess


class Imdb_spider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    custom_settings = {'FEEDS': {'IMDBTop250.csv': {"format": 'csv','overwrite': True}}}

    def parse(self, response):
        number = 0
        for href in response.css("td.titleColumn a::attr(href)").getall():
            item = Imdb_item()
            item['title'] = response.css("td.titleColumn a::text").getall()[number]
            item['movie_id'] = response.css("td.watchlistColumn div::attr(data-tconst)").getall()[number]
            item ['year'] = response.css("td.titleColumn span::text").getall()[number][1:5]
            item['rating'] = response.css("td.posterColumn span[name=ir]::attr(data-value)").getall()[number]
            item['rank'] = response.css("td.posterColumn span[name=rk]::attr(data-value)").getall()[number]
            number += 1
            request = scrapy.Request(response.urljoin(href),callback=self.parse_movie, cb_kwargs=dict(movie=item))
            yield request

    def parse_movie(self, response, movie):
        movie['movie_link'] = response.url
        movie['genre'] = response.xpath("//li[@data-testid='storyline-genres']/div/ul/li/a/text()").getall()
        movie['runtime'] = response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall()
        movie['budget'] = response.xpath("//li[@data-testid='title-boxoffice-budget']/div/ul/li/span/text()").getall()
        movie['origin'] = response.xpath("//li[@data-testid='title-details-origin']/div/ul/li/a/text()").getall()
        movie['mpaa_rating'] = response.xpath("//ul[@data-testid='hero-title-block__metadata']/li[2]/a/text()").getall()
        return movie


# Code to make script run like normal Python script
process = CrawlerProcess()
process.crawl(Imdb_spider)
process.start()  # the script will block here until the crawling is finished
