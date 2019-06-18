# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy.http.request import Request
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline
from TapTap import settings


"""
class TaptapPipeline(object):
    def __init__(self):
        self.fp = open('item.json', 'wb')
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False)

    def start_exporting(self):
        pass

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def end_exporting(self):
        pass
"""

class TaptapCsvExporter(CsvItemExporter):
    def __init__(self):
        self.fp = open("export.csv", "wb")
        kwargs = {"fields_to_export": ["name", "introduction", "points", "publisher", "author", "setup_count",
                                       "follower_count", "booking_count", "tag_names", "update_log", "app_size",
                                       "version", "last_update"],
                  "encoding": "utf-8"}
        super().__init__(self.fp, **kwargs)


class TaptapCsvPipeline(object):
    def __init__(self):
        self.csv_exporter = TaptapCsvExporter()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item


class PicsDownloadPipeline(ImagesPipeline):

    DEFAULT_IMAGES_URLS_FIELD = 'screen_shots'

    def get_media_requests(self, item, info):
        # thumbnail、screen_shots        # 缩略图、截图
        request_objs = super().get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
            request_obj.item_category = "screen_shots"

        request_obj = Request(item["thumbnail"])
        request_obj.item = item
        request_obj.item_category = "thumbnail"
        request_objs.append(request_obj)

        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super().file_path(request, response, info)
        item = request.item

        category_path = os.path.join(settings.IMAGES_STORE, item["name"])
        thumbnail_path = os.path.join(category_path, "thumbnail")
        shots_path = os.path.join(category_path, "screen_shots")
        if not os.path.exists(category_path):
            os.mkdir(category_path)
            os.mkdir(thumbnail_path)
            os.mkdir(shots_path)

        # 判断是截图还是缩略图
        if request.item_category == "thumbnail":
            path = thumbnail_path
        else:
            path = shots_path

        uri, qs = request.url.split('?')
        image_name = uri.split('/')[-1]
        image_path = os.path.join(path, image_name)

        return image_path
