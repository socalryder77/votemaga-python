# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class StateGovBriefingsSpider(scrapy.Spider):
    name = 'state_gov_briefings'
    start_urls = ['https://www.state.gov/r/pa/prs/dpb/index.htm']

    def parse(self, response):
        items = []
        for element in response.css("div.event-desc a.read")[-self.settings.attributes['SCRAPE_LIMIT'].value:]:
            item = NewsRelease()
            item['link'] = element.css('::attr(href)').extract_first()
            request = scrapy.Request(item['link'], callback=self.parse_title)
            request.meta['item'] = item
            items.append(request)
        return items

    def parse_title(self, response):
        item = response.meta['item']
        item['title'] = response.css("h2#page-title::text").extract_first()
        return item
