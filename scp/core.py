# -*- coding: utf-8 -*-

from .db_constants import DB_NAME, TEST_DB_NAME, CREATE_DB_SCP_SQL, CREATE_DB_DETAIL_SQL, CREATE_COLLECTION_DB_SQL, CREATE_TAG_DB_SQL
from .util import *


# 初始化数据库
def init_database():
    if not os.path.exists(DB_NAME):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(CREATE_DB_SCP_SQL)
        cur.execute(CREATE_DB_DETAIL_SQL)
        cur.execute(CREATE_COLLECTION_DB_SQL)
        cur.execute(CREATE_TAG_DB_SQL)
        con.commit()
        con.close()
    if not os.path.exists(TEST_DB_NAME):
        test_con = sqlite3.connect(TEST_DB_NAME)
        test_cur = test_con.cursor()
        test_cur.execute(CREATE_DB_SCP_SQL)
        test_cur.execute(CREATE_DB_DETAIL_SQL)
        test_cur.execute(CREATE_COLLECTION_DB_SQL)
        test_cur.execute(CREATE_TAG_DB_SQL)
        test_con.commit()
        test_con.close()


class ScpSpider:
    def __init__(self) -> None:
        # init database file
        init_database()

    def crawl_this_spider(self, spider_name):
        os.system('cd scp/scrapy_spider && scrapy crawl ' + spider_name)

    # def crawl_main_list(self):
    #     # use scrapy crawl scp list and save in db
    #     os.system('cd scp/scrapy_spider && scrapy crawl main_list_spider')
    #
    # def crawl_main_detail(self):
    #     os.system('cd scp/scrapy_spider && scrapy crawl detail_spider')
    #
    # def crawl_single_pages(self):
    #     os.system('cd scp/scrapy_spider && scrapy crawl single_page_spider')
    #
    # def crawl_offset_pages(self):
    #     os.system('cd scp/scrapy_spider && scrapy crawl offset_spider')
    #
    # def crawl_collection_pages(self):
    #     os.system('cd scp/scrapy_spider && scrapy crawl collection_spider')
