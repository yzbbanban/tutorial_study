# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # 项目唯一名
    allowed_domains = ['quotes.toscrape.com']  # 允许爬取的域名
    start_urls = ['http://quotes.toscrape.com/']  # 启动时爬取的域名，初始请求

    # 初始请求结束时调用
    def parse(self, response):
        pass
