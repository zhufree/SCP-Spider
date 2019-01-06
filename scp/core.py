# -*- coding: utf-8 -*-

from .constants import DB_NAME, CREATE_DB_SQL, CREATE_COLLECTION_DB_SQL, CREATE_TAG_DB_SQL
import sqlite3
import os


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
# ScpSpider().crawl_main_list()
