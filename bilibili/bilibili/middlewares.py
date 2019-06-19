# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http.response.html import HtmlResponse
from bilibili.settings import CHROME_DRIVER_PATH


class BilibiliDownloaderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    def process_request(self, request, spider):
        self.driver.get(request.url)

        if "/video/av" in request.url:
            # 视频详情界面
            self.dont_excepted_text((By.CLASS_NAME, "dm"), "--弹幕")
            self.extension_load()

        source = self.driver.page_source
        response = HtmlResponse(request.url, body=source, request=request, encoding="utf-8")

        return response

    def dont_excepted_text(self, locator, text, timeout=10):
        """ 直到元素的文本不为期望文本"""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.text_to_be_present_in_element(locator, text))
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout=10):
        """ html元素是否可见，判断是否已加载成功"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def extension_load(self):
        """ 延伸加载数据，例如有些需要点击发送ajax请求的按钮"""
        pass
