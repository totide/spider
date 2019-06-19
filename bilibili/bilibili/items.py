# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    play_count = scrapy.Field()
    barrage_count = scrapy.Field()
    like_count = scrapy.Field()
    throw_coin_count = scrapy.Field()
    collection_count = scrapy.Field()
    tag_names = scrapy.Field()
    comment_count = scrapy.Field()
    publish_time = scrapy.Field()
