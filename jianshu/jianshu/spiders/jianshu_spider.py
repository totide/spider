# -*- coding: utf-8 -*-

import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem
from scrapy_redis.spiders import RedisCrawlSpider


class JianshuSpiderSpider(RedisCrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    #start_urls = ['https://www.jianshu.com/']
    redis_key = "jianshu:start_urls"
    pattern = re.compile(r".*?(\d+)")

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        """ 解析详情页信息"""
        article_tag = response.xpath("//div[@class='article']")
        # 标题
        title = article_tag.xpath("./h1[@class='title']/text()").get()
        # 作者
        author = article_tag.xpath(".//span[@class='name']/a/text()").get()
        # 发布时间
        publish_time = article_tag.xpath(".//span[@class='publish-time']/text()").get().replace('*', '')
        #  字数、 阅读数、 评论数、 喜欢数
        word_count = article_tag.xpath(".//span[@class='wordage']/text()").get()
        view_count = article_tag.xpath(".//span[@class='views-count']/text()").get()
        comment_count = article_tag.xpath(".//span[@class='comments-count']/text()").get()
        like_count = article_tag.xpath(".//span[@class='likes-count']/text()").get()
        counts = [word_count, view_count, comment_count, like_count]
        word_count, view_count, comment_count, like_count = map(lambda x: re.search(self.pattern, x).group(1), counts)
        # 内容
        content = "".join(article_tag.xpath(".//div[@class='show-content-free']//text()").getall()).strip()
        # 专题(因为有些专题有逗号，因此用分号进行连接)
        subjects = ";".join(response.xpath("//div[@class='include-collection']/a/div/text()").getall())

        info = {
            "title": title,
            "author": author,
            "publish_time": publish_time,
            "word_count": word_count,
            "view_count": view_count,
            "comment_count": comment_count,
            "like_count": like_count,
            "content": content,
            "subjects": subjects
        }
        yield JianshuItem(**info)
