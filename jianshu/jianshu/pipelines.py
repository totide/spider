# -*- coding: utf-8 -*-

from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuPipeline(object):
    def __init__(self):
        db_params = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "123456",
            "database": "jianshu",
            "charset": "utf8",
            "cursorclass": cursors.DictCursor
        }
        self.db_pool = adbapi.ConnectionPool("pymysql", **db_params)
        self._sql = ""

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(title, author, publish_time, word_count, view_count,
                                    comment_count, like_count, content, subjects)
                                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        return self._sql

    def process_item(self, item, spider):
        defer = self.db_pool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handler_error, item, spider)
        return item

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item["title"], item["author"], item["publish_time"],
                                  item["word_count"], item["view_count"], item["comment_count"],
                                  item["like_count"], item['content'], item["subjects"]))

    def handler_error(self, error, item, spider):
        print(self.sql, error, item, spider)
