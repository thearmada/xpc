# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['http://www.xinpianchang.com/channel/index/sort-like']
    start_urls = ['http://http://www.xinpianchang.com/channel/index/sort-like/']

    def parse(self, response):
        pass
