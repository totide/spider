# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from pymysql import cursors


class BilibiliPipeline(object):
    def __init__(self):
        db_params = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "123456",
            "database": "bilibili",
            "charset": "utf8",
            "cursorclass": cursors.DictCursor
        }
        self.db_pool = adbapi.ConnectionPool("pymysql", **db_params)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into video(title, category, play_count, barrage_count, like_count, 
                                  throw_coin_count, collection_count, comment_count, tag_names, publish_time) 
                                  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        return self._sql

    def process_item(self, item, spider):
        defer = self.db_pool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handler_error, item, spider)
        return item

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item["title"], item["category"], item["play_count"], item["barrage_count"],
                                  item["like_count"], item["throw_coin_count"], item["collection_count"],
                                  item["comment_count"], item["tag_names"], item["publish_time"]))

    def handler_error(self, error, item, spider):
        print(error, item, spider)
