# -*- coding: utf-8 -*-
import scrapy
from news_releases.items import NewsRelease

class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    custom_settings = {'EXPECTED':9}
    start_urls = ['https://twitter.com/potus',
                  'https://twitter.com/realDonaldTrump',
                  'https://twitter.com/WhiteHouse']

    def parse(self, response):
        items = []
        for element in response.css('ol#stream-items-id li div.tweet')[:self.settings.attributes['SCRAPE_LIMIT'].value]:
            item = NewsRelease()
            text = element.xpath("div[@class='content']/div[@class='js-tweet-text-container']//text()[not(ancestor-or-self::a[contains(@class, 'u-hidden')])]").extract()
            good_text = ""
            for part in text:
                if "\n" not in part:
                    good_text += part
            item['title'] = good_text
            item['link'] = 'https://www.twitter.com' + element.css('::attr(data-permalink-path)').extract_first()
            items.append(item)
        return items
