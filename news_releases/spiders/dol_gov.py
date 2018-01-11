# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class DOLGovSpider(scrapy.Spider):
    name = 'dol_gov'
    start_urls = ['https://www.dol.gov/newsroom/releases']

    def parse(self, response):
        items = []
        for element in response.css('div.field-name-title div.field-items div.field-item a')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.dol.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return items
