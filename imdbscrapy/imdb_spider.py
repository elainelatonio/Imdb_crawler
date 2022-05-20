import scrapy
from items import Imdb_item
from scrapy.crawler import CrawlerProcess
import re


class Imdb_spider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    custom_settings = {'FEEDS': {'IMDBTop250_v2.csv': {"format": 'csv','overwrite': True}}}

    def parse(self, response):
        number = 0
        titles = response.css("td.titleColumn a::text").getall()
        movie_ids = response.css("td.watchlistColumn div::attr(data-tconst)").getall()
        years = response.css("td.titleColumn span::text").getall()
        ratings = response.css("td.posterColumn span[name=ir]::attr(data-value)").getall()
        votes = response.css("td.posterColumn span[name=nv]::attr(data-value)").getall()
        ranks = response.css("td.posterColumn span[name=rk]::attr(data-value)").getall()
        for href in response.css("td.titleColumn a::attr(href)").getall():
            item = Imdb_item()
            item['title'] = titles[number]
            item['movie_id'] = movie_ids[number]
            item['year'] = years[number][1:5]
            item['rating'] = ratings[number]
            item['votes'] = votes[number]
            item['rank'] = ranks[number]
            number += 1
            request = scrapy.Request(response.urljoin(href),callback=self.parse_movie, cb_kwargs=dict(movie=item))
            yield request

    def parse_movie(self, response, movie):
        movie['movie_link'] = response.url
        movie['genre'] = response.xpath("//li[@data-testid='storyline-genres']/div/ul/li/a/text()").getall()
        movie['runtime_mins'] = (int(response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall()[0])*60
                                 if 'hours' in response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall()
                                 else 0) + (int(re.findall('(\d+) minutes',''.join(map(str,response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall())))[0])
                                if 'minutes' in response.xpath("//li[@data-testid='title-techspec_runtime']/div/text()").getall() else 0)
        # movie['budget'] = response.xpath("//li[@data-testid='title-boxoffice-budget']/div/ul/li/span/text()").getall()
        movie['origin'] = response.xpath("//li[@data-testid='title-details-origin']/div/ul/li/a/text()").getall()
        movie['awards_wins'] = ''.join(map(str,(re.findall('(\d+) wins', response.xpath("//li[@data-testid='award_information']/div/ul/li/span/text()").getall()[0],re.IGNORECASE))))
        movie['awards_nominations'] = ''.join(map(str,(re.findall('(\d+) nominations', response.xpath("//li[@data-testid='award_information']/div/ul/li/span/text()").getall()[0],re.IGNORECASE))))
        movie['gross_worldwide_usd'] = response.xpath("//li[@data-testid='title-boxoffice-cumulativeworldwidegross']"
                                                      "/div/ul/li/span/text()").get().replace('$','') if response.xpath("//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div/ul/li/span/text()").get() != None else 0
        return movie


# Code to make script run like normal Python script
process = CrawlerProcess()
process.crawl(Imdb_spider)
process.start()  # the script will block here until the crawling is finished
