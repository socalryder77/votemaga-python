# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease
import pdb
class TreasuryGovSpider(scrapy.Spider):
    name = 'treasury_gov'
    custom_settings = {'EXPECTED': 6}
    start_urls = ['https://www.treasury.gov/press-center/press-releases/Pages/default.aspx',
                  'https://www.treasury.gov/press-center/news/Pages/default.aspx']

    def parse(self, response):
        items = []
        for element in response.xpath("//table[@class='t-press']/tr[contains(@class, 'datarow')]/td[2]/a")[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.treasury.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return items
