# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

from .db_constants import ensure_databases

SCP_DIR = Path(__file__).resolve().parent


def init_database():
    ensure_databases()


def crawl_this_spider(spider_name):
    if str(SCP_DIR) not in sys.path:
        sys.path.insert(0, str(SCP_DIR))
    os.environ["SCRAPY_SETTINGS_MODULE"] = "scrapy_spider.settings"
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name)
    process.start()
