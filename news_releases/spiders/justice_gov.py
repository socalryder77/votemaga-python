# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class JusticeGovSpider(scrapy.Spider):
    name = 'justice_gov'
    custom_settings = {'EXPECTED': 3}
    start_urls = ['https://www.justice.gov/news']    

    def parse(self, response):
        items = []
        for element in response.css('span.field-content a')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.justice.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return items
