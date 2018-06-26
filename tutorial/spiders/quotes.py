# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # 项目唯一名
    allowed_domains = ['quotes.toscrape.com']  # 允许爬取的域名
    start_urls = ['http://quotes.toscrape.com/']  # 启动时爬取的域名，初始请求

    # 初始请求结束时调用
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
        # pass
