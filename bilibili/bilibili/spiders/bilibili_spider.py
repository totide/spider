# -*- coding: utf-8 -*-

import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bilibili.items import BilibiliItem


class BilibiliSpiderSpider(CrawlSpider):
    name = 'bilibili_spider'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/v/game']

    rules = (
        Rule(LinkExtractor(allow=r'.*/v/game/.*'), follow=True),
        Rule(LinkExtractor(allow=r'.*/video/av[0-9]{7,8}'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        div = response.xpath("//div[@id='viewbox_report']")
        # 标题
        title = div.xpath(".//span/text()").get()
        # 视频分类
        category = ">".join(div.xpath(".//span[@class='a-crumbs']/a/text()").getall())
        # 发布时间
        publish_time = div.xpath(".//div[1]/span[2]/text()").get()
        # 播放数
        play_text = div.xpath(".//span[contains(@title, '播放数')]/text()").get()
        play_count = re.sub(r"播放.*", "", play_text)
        # 弹幕数
        barrage_text = div.xpath(".//span[contains(@title, '弹幕数')]/text()").get()
        barrage_count = re.sub(r"弹幕.*", "", barrage_text)
        # 点赞数、投硬数、收藏数
        ops_list = [x.strip() for x in response.xpath("//div[@class='ops']/span/text()").getall()]
        like_count = ops_list[0] if ops_list[0] != "点赞" else "0"
        throw_coin_count = ops_list[1] if ops_list[1] != "投币" else "0"
        collection_count = ops_list[2] if ops_list[2] != "收藏" else "0"
        # 评论数
        comment_count = response.xpath("//meta[@itemprop='commentCount']/@content").get()
        # 标签列表
        tag_text = response.xpath("//ul[contains(@class, 'tag-area')]/li//text()").getall()
        tag_names = ",".join(tag_text)

        info = {
            "title": title,
            "category": category,
            "publish_time": publish_time,
            "play_count": play_count,
            "barrage_count": barrage_count,
            "like_count": like_count,
            "throw_coin_count": throw_coin_count,
            "collection_count": collection_count,
            "comment_count": comment_count,
            "tag_names": tag_names
        }
        for k, v in info.copy().items():
            if ("_count" in k) and ("万" in v):
                info[k] = int(float(v.replace("万", "")) * 10000)

        yield BilibiliItem(**info)



