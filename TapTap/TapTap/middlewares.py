# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random


class UserAgentDownloadMiddleware(object):
    User_AGENTS = [
        "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
        "Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
        "Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1)",
        "AmigaVoyager/3.2 (AmigaOS/MC680x0)",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.User_AGENTS)
        request.headers['User-Agent'] = user_agent


"""
class ProxyDownloadMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = ''

    def process_response(self, request, response, spider):
        if response.status != 200:
            self.update_proxy()
            return request

        return response

    def update_proxy(self):
        pass
"""