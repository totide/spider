# -*- coding: utf-8 -*-

import scrapy


class JianshuItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    word_count = scrapy.Field()
    view_count = scrapy.Field()
    comment_count = scrapy.Field()
    like_count = scrapy.Field()
    content = scrapy.Field()
    subjects = scrapy.Field()
