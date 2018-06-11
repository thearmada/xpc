# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['http://www.xinpianchang.com/channel/index/sort-like']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like/']

    def parse(self, response):
        #取出列表页的所有视频节点
        url = "http://www.xinpianchang.com/a%s?from=ArticleList"
        posts = response.xpath('//ul[@class="video-list"]/li')
        #循环便利所有节点，每个节点对应每一个视频
        for post in posts:
        	pid = post.xpath('./@data-articleid').extract_first()
        	#根据ID拼接处视频的详情页
        	request = Request(url % pid, callback=self.parse_post)
        	#利用request.meta属性的作用，将pid传递给回调函数
        	request.meta['pid'] = pid
        	#将列表页的缩列图传递给回调函数
        	request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
        	print(request.meta)
        	#yield request

    def parse_post(self, response):
    	pass