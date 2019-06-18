# -*- coding: utf-8 -*-

import json
import re
import scrapy
from urllib import parse
from lxml import etree

from TapTap.items import TagItem


class TaptapSpiderSpider(scrapy.Spider):
    name = 'taptap_spider'
    allowed_domains = ['taptap.com']
    start_urls = ['http://www.taptap.com/']
    tag_info_url = "https://www.taptap.com/ajax/search/tags?"

    def parse(self, response):
        """ 获取所有标签的名称和链接地址"""
        tags = response.xpath("//div[@class='index-tag-body']/ul/li/a")
        for tag in tags:
            tag_name = tag.xpath(".//text()").get().strip()
            tag_url = tag.xpath(".//@href").get().strip()
            yield scrapy.Request(tag_url, callback=self.parse_tag,
                                 meta={"info": {"tag_name": tag_name}})

    def parse_tag(self, response):
        """ 通过ajax发起获取标签信息的请求"""
        tag_name = response.meta.get("info")["tag_name"]
        data = {"kw": tag_name, "sort": "hits", "page": 1}
        qs = parse.urlencode(data)
        info_url = self.tag_info_url+qs
        yield scrapy.Request(info_url, callback=self.parse_tag_info,
                             meta={"info": {"tag_name": tag_name}})

    def parse_tag_info(self, response):
        """ 解析标签简述内容获取详情url"""
        info = json.loads(response.text)
        html = info["data"]["html"]
        next = info["data"]["next"]

        tag_name = response.meta.get("info")["tag_name"]
        tag_info = etree.HTML(html)
        divs = tag_info.xpath("//div[@class='taptap-app-card']")
        for div in divs:
            detail_url = div.xpath("./a/@href")[0]
            yield scrapy.Request(detail_url, callback=self.parse_game_detail)

        if next:
            yield scrapy.Request(next, callback=self.parse_tag_info,
                                 meta={"info": {"tag_name": tag_name}})

    def parse_game_detail(self, response):
        """ 获取游戏详情信息"""
        booking_count = 0
        follower_count = 0
        setup_count = 0
        count_pattern = re.compile(r"(\d+).*")

        thumbnail = response.xpath("//img[@itemprop='image']/@src").get()
        publisher = response.xpath("//a[@itemprop='publisher']/span[@itemprop='name']/text()").get()
        author = response.xpath("//div[@class='header-text-author']//span[@itemprop='name']/text()").get()
        points = response.xpath("//span[@itemprop='ratingValue']/text()").get()
        name = response.xpath("//h1[@itemprop='name']/text()").get().strip()
        tag_list = response.xpath("//ul[@id='appTag']//a/text()").getall()
        tag_names = ",".join(map(lambda x: re.sub(r"\s", "", x), tag_list))
        description = response.xpath("//p[@class='description']//text()").getall()
        description = map(lambda x: re.sub(r"\s", "", x), description)
        for desc in description:
            if "预约" in desc:
                booking_count = re.search(count_pattern, desc).group(1)
            elif "关注" in desc:
                follower_count = re.search(count_pattern, desc).group(1)
            elif "安装" in desc:
                setup_count = re.search(count_pattern, desc).group(1)

        # 屏幕截图
        screen_shots = response.xpath("//ul[@id='imageShots']//img/@src").getall()
        introduction = "".join(response.xpath("//div[@id='description']//text()").getall()).strip()
        detail_title = response.xpath(
            "//ul[@class='list-unstyled body-info-list']/li/span[@class='info-item-title']/text()").getall()
        detail_content = response.xpath(
            "//ul[@class='list-unstyled body-info-list']/li/span[@class='info-item-content']/text()").getall()
        detail = dict(zip(detail_title, detail_content))

        app_size = detail.get("文件大小:", "")
        version = detail.get("当前版本:", "")
        last_update = detail.get("更新时间:", "")

        item_info = {
            "publisher": publisher,
            "author": author,
            "thumbnail": thumbnail,
            "points": points,
            "name": name,
            "tag_names": tag_names,
            "booking_count": booking_count,
            "follower_count": follower_count,
            "setup_count": setup_count,
            "screen_shots": screen_shots,
            "introduction": introduction,
            "app_size": app_size,
            "version": version,
            "last_update": last_update
        }
        yield TagItem(**item_info)
