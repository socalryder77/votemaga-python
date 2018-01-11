# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class DOIGovSpider(scrapy.Spider):
    name = 'doi_gov'
    custom_settings = {'EXPECTED': 3}
    start_urls = ['https://www.doi.gov/news']

    def parse(self, response):
        
        items = []
        for element in response.css('div.node-press-release div.node__content div.node-title a')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.doi.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return []
