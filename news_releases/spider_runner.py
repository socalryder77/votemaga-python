# -*- coding: utf-8 -*-
import sys
import logging
import traceback
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.whitehouse_statements import WhitehouseStatementsSpider
from spiders.youtube import YoutubeSpider
from spiders.donaldjtrump import DonaldjtrumpSpider
from spiders.twitter import TwitterSpider
from spiders.dhs_gov import DHSGovSpider
from spiders.commerce_gov import CommerceGovSpider
from spiders.defense_gov import DefenseGovSpider
from spiders.education_gov import EducationGovSpider
from spiders.usda_gov import USDAGovSpider
from spiders.energy_gov import EnergyGovSpider
from spiders.hhs_gov_news import HHSGovNewsSpider
from spiders.hhs_gov_blog import HHSGovBlogSpider
from spiders.state_gov import StateGovSpider
from spiders.state_gov_briefings import StateGovBriefingsSpider
from spiders.hud_gov import HUDGovSpider
from spiders.justice_gov import JusticeGovSpider
from spiders.dol_gov import DOLGovSpider
from spiders.dol_gov_blog import DOLGovBlogSpider
from spiders.transportation_gov import TransportationGovSpider
from spiders.transportation_gov_blog import TransportationGovBlogSpider
from spiders.va_gov import VAGovSpider
from spiders.doi_gov import DOIGovSpider
from spiders.treasury_gov import TreasuryGovSpider
from spiders.cia_gov import CIAGovSpider
from spiders.epa_gov import EPAGovSpider
from spiders.dni_gov import DNIGovSpider
from spiders.sba_gov import SBAGovSpider
from spiders.sec_gov import SECGovSpider
from spiders.west_wing_reads import WestWingReadsSpider
from spiders.fbi_gov import FBIGovSpider
from spiders.whitehouse_news import WhitehouseNewsSpider

from scrapy.conf import settings
import io
import json
import os

class SpiderRunner():
    def __init__(self):
        self.SPIDER_LIST = [
            WhitehouseStatementsSpider, YoutubeSpider, DonaldjtrumpSpider, TwitterSpider, DHSGovSpider,
            CommerceGovSpider, DefenseGovSpider, EducationGovSpider, USDAGovSpider, EnergyGovSpider, HHSGovNewsSpider,
            HHSGovBlogSpider, StateGovSpider, StateGovBriefingsSpider, HUDGovSpider, JusticeGovSpider, DOLGovSpider,
            DOLGovBlogSpider, TransportationGovSpider, TransportationGovBlogSpider, VAGovSpider, DOIGovSpider,
            TreasuryGovSpider, CIAGovSpider, EPAGovSpider, DNIGovSpider, SBAGovSpider, SECGovSpider,
            FBIGovSpider, WhitehouseNewsSpider
        ]

        # This array does nothing
        # It's just to keep track of which spiders need to be worked on
        # - socal
        brokenSpiders = [
            # westwing reads is now just a static page and the markup structure may be inconsistent
            # TODO: Figure out something for WestWingReads
            WestWingReadsSpider
        ]

    def run_spiders(self):
        try:
            settings.overrides.update({'SCRAPE_LIMIT': 3,
                                       'LOG_LEVEL': 'DEBUG',
                                       'USER_AGENT': 'JrodManU (+https://github.com/JrodManU)',
                                       'ROBOTSTXT_OBEY': False,
                                       'ITEM_PIPELINES': { 'news_releases.pipelines.JsonPipeline': 300 },
                                       'DOWNLOAD_TIMEOUT': 12,
                                       'DNS_TIMEOUT': 12,
                                       'RETRY_ENABLED': False
                                       })
            ## set up the crawler and start to crawl one spider at a time
            process = CrawlerProcess(settings)
            for spider in self.SPIDER_LIST:
                process.crawl(spider)
            process.start()
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.info('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            logging.info("Exception: %s" % str(traceback.format_exc()))

    def get_data(self):
        data = {}
        for spider in self.SPIDER_LIST:
            data_file = None
            data[spider.name] = []
            try:
                data_file = io.open(os.path.join(os.path.dirname(__file__), "results/" + spider.name + '.json'), 'r', encoding='utf-8')
                line = data_file.readline()
                if line != u'':
                   data[spider.name] = json.loads(line)
            except Exception:
                data_file = io.open(os.path.join(os.path.dirname(__file__), "results/" + spider.name + '.json'), 'w', encoding='utf-8')
            data_file.close()
        return data

    def get_spider_list(self):
        return self.SPIDER_LIST
