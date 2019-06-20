# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http.response.html import HtmlResponse
from jianshu.settings import CHROME_DRIVER_PATH


class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    def process_request(self, request, spider):
        if "/p/" in  request.url:
            self.driver.get(request.url)
            self.is_visible("//span[@class='views-count']")
            self.is_visible("//div[@class='include-collection']")

            try:
                while True:
                    # 收录专题有“展开更多”按钮，将模拟点击进行展开数据
                    show_more = self.driver.find_element_by_class_name("show-more")
                    if show_more:
                        show_more.click()
                        time.sleep(0.5)
                    else:
                        break
            except:
                pass

            return HtmlResponse(request.url, body=self.driver.page_source, request=request, encoding="utf-8")

    def is_visible(self, locator, timeout=10):
        """ 网站元素是否存在"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False
