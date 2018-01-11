# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class HUDGovSpider(scrapy.Spider):
    name = 'hud_gov'
    custom_settings = {'EXPECTED': 6}
    start_urls = ['https://portal.hud.gov/hudportal/HUD?src=/press/speeches_remarks_statements',
                  'https://portal.hud.gov/hudportal/HUD?src=/press/press_releases_media_advisories']

    def parse(self, response):
        items = []
        for element in response.css('div.hudpagepad div.genlink a')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            item['title'] = element.css('::text').extract_first()
            item['link'] = element.css('::attr(href)').extract_first()
            items.append(item)
        return items
