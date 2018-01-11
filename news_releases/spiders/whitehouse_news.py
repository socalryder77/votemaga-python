# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease


class WhitehouseNewsSpider(scrapy.Spider):
    name = 'whitehouse_news'
    start_urls = ['https://www.whitehouse.gov/news/']


    def parse(self, response):
        items = []
        for element in response.css('div.page-results__wrap article'):
            item = NewsRelease()
            item['link'] = element.css('::attr(href)').extract_first()
            request = scrapy.Request(item['link'], callback=self.whitehouse_news_title)
            request.meta['item'] = item
            items.append(request)
        return items

    def whitehouse_news_title(self, response):
        item = response.meta['item']
        item['title'] = response.css('title::text').extract_first()
        return item
