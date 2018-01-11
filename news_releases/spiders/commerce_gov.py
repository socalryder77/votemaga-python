# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class CommerceGovSpider(scrapy.Spider):
    name = 'commerce_gov'
    start_urls = ['https://www.commerce.gov/news']

    def parse(self, response):
        items = []
        for element in response.css('article.article div div div div div div div h2 a')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.commerce.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return items
