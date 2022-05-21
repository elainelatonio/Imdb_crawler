# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Imdb_item(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    movie_id = scrapy.Field()
    movie_link = scrapy.Field()
    rating = scrapy.Field()
    genre = scrapy.Field()
    runtime_mins = scrapy.Field()
    origin = scrapy.Field()
    votes = scrapy.Field()
    awards_wins = scrapy.Field()
    awards_nominations = scrapy.Field()
    gross_worldwide_usd = scrapy.Field()
