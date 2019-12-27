# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    username = scrapy.Field()
    country = scrapy.Field()
    review_date = scrapy.Field()
    score = scrapy.Field()
    room_info = scrapy.Field()
    good = scrapy.Field()
    poor = scrapy.Field()
    createdAt = scrapy.Field()
    
