# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TagItem(scrapy.Item):
    name = scrapy.Field()                   # 游戏名
    thumbnail = scrapy.Field()              # 缩略图
    setup_count = scrapy.Field()            # 安装数
    follower_count = scrapy.Field()         # 关注数
    booking_count = scrapy.Field()          # 预约数
    points = scrapy.Field()                 # 评分
    publisher = scrapy.Field()              # 发行商
    author = scrapy.Field()                 # 开发商
    tag_names = scrapy.Field()              # 所属标签列表
    screen_shots = scrapy.Field()           # 截图
    introduction = scrapy.Field()           # 简介
    update_log = scrapy.Field()             # 更新日志
    app_size = scrapy.Field()               # 应用大小
    version = scrapy.Field()                # 版本号
    last_update = scrapy.Field()            # 最新更新时间


