# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class StateGovSpider(scrapy.Spider):
    name = 'state_gov'
    custom_settings = {'EXPECTED': 6}
    start_urls = ['https://www.state.gov/r/pa/prs/sb/index.htm',
                  'https://www.state.gov/r/pa/ei/opeds/index.htm']

    def parse(self, response):
        items = []
        for element in response.xpath("//div[@class='l-wrap']/a[@target='_self']|//div[@class='l-wrap']/p/a[@target='_self']")[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = "https://www.state.gov" + element.css('::attr(href)').extract_first()
            items.append(item)
        return items
