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
        	#print(request.meta)
        	yield request

    def parse_post(self, response):
    	#创建一个Item对象
    	post = {}
    	#取出上一步函数传递过来的值
    	post['pid'] = response.meta['pid']
    	#提取头像
    	post['thumbnail'] = response.meta['thumbnail']
    	#提取处预览图
    	post['preview'] = response.xpath('//div[@class="filmplay"]//img/@src').get()
    	#视频url
    	post['video'] = response.xpath('//a[@id="player"]/@href').get()
    	#视频标题
    	post['title'] = response.xpath('//div[@class="filmplay-info"]//h3/text()').get()
    	#视频分类，由于取出的是多个，需要先strip,再join
    	caegory = response.xpath('//span[contains(@class, "cate")]//text()').extract()
    	post['category'] = ''.join([strip(c) for c in category]).strip()
    	#创建时间
    	post['created_at'] = response.xpath('//span[contains(@class,  "update-time")]/i/text()').get()
    	#播放次数
    	post['play_counts'] = response.xpath('//i[contains(@class, "play_counts"]/@data-curplaycounts').get()
    	#该视频被点赞次数
    	post['likecounts'] = response.xpath('//span[contains(@class, "like-counts")/@data-counts]').get()
    	#描述
    	post['description'] = strip(response.xpath('//p[contains(@class, "desc")]/text()').get())
    	yield post

    	#z作者url的模板
    	url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
    	#取出所有的作者节点
    	composers = response.xpath('//ul[@class="creater-list"]/li')
    	for composer in composers:
    		#取出作者的ID
    		cid = composer.xpath('./a/@data-userid').get()
    		#瓶装成作者的主页url，并创建request对象
    		request = Request(url % cid, callback=self.parse_composer)
    		#把cid传递给回调函数
    		request.meta['cid'] = cid
    		yield request

    def parse_composer(self, response):
    	composer = {}
    	composer['cid'] = response.meta['cid']
    	#取一下用户主页的背景大图
    	background = response.xpath('//div[@class="banner-wrap"]/@style').get()
    	#因为大图是写在css样式里的， 所以用切片操作提取出来
    	composer['banner'] = background[21:-1]
    	#用户头像
    	composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
    	#用户名称
    	composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get()
    	#自我介绍
    	composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
    	#用户人气，也就是被点赞的次数综合
    	composer['like_counts'] = ci(response.xpath('//span[contains(@class, "like_counts")]/text()').get())
    	#关注他的用户数量
    	composer['follow_counts'] = ci(response.xpath('//spqn[@class="follow-wrap"]/spqn[2]/test()')).get()
    	#所在位置
    	composer['career'] = response.xpath('//span[contains(@class, "icon-career")]/'
    										'following-sibling::span[1]/text()').get()
    	yield composer

