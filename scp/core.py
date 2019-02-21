# -*- coding: utf-8 -*-

from .constants import DB_NAME, CREATE_DB_SQL, CREATE_COLLECTION_DB_SQL, CREATE_TAG_DB_SQL
import sqlite3
import os
from .util import *


def init_database():
    if not os.path.exists(DB_NAME):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(CREATE_DB_SQL)
        cur.execute(CREATE_COLLECTION_DB_SQL)
        cur.execute(CREATE_TAG_DB_SQL)
        con.commit()
        con.close()


class ScpSpider:
    def __init__(self) -> None:
        # init database file
        init_database()

    def crawl_main_list(self):
        # use scrapy crawl scp list and save in db
        os.system('cd scp/scrapy_spider && scrapy crawl main_list_spider')

    def crawl_main_detail(self):
        os.system('cd scp/scrapy_spider && scrapy crawl detail_spider')

    def crawl_single_pages(self):
        os.system('cd scp/scrapy_spider && scrapy crawl single_page_spider')

    def crawl_offset_pages(self):
        os.system('cd scp/scrapy_spider && scrapy crawl offset_spider')

    def crawl_collection_pages(self):
        os.system('cd scp/scrapy_spider && scrapy crawl collection_spider')

    def split_csv(self):
        split_csv_file('scps.csv')

    def set_download_type(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("update scps set download_type = 0 where scp_type = 1;")
        cur.execute("update scps set download_type = 1 where scp_type = 2;")
        cur.execute("update scps set download_type = 2 where scp_type in (3,4);")
        cur.execute("update scps set download_type = 3 where scp_type in (0,5,6,7,8,9,10,11,12);")
        cur.execute("update scps set download_type = 4 where scp_type in (16,18);")
        cur.execute("update scp_collection set download_type = 4;")
        con.commit()
        con.close()

# ScpSpider().crawl_main_list()
