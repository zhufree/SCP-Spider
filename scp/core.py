# -*- coding: utf-8 -*-

from .db_constants import CATE_DB_NAME, TEST_DB_NAME, DETAIL_DB_NAME, CREATE_DB_SCP_SQL, CREATE_DB_DETAIL_SQL
from .util import *


# 初始化数据库
def init_database():
    if not os.path.exists(CATE_DB_NAME):
        con = sqlite3.connect(CATE_DB_NAME)
        cur = con.cursor()
        cur.execute(CREATE_DB_SCP_SQL)
        # cur.execute(CREATE_DB_DETAIL_SQL)
        con.commit()
        con.close()
    if not os.path.exists(DETAIL_DB_NAME):
        con = sqlite3.connect(DETAIL_DB_NAME)
        cur = con.cursor()
        # cur.execute(CREATE_DB_SCP_SQL)
        cur.execute(CREATE_DB_DETAIL_SQL)
        con.commit()
        con.close()
    if not os.path.exists(TEST_DB_NAME):
        test_con = sqlite3.connect(TEST_DB_NAME)
        test_cur = test_con.cursor()
        test_cur.execute(CREATE_DB_SCP_SQL)
        test_cur.execute(CREATE_DB_DETAIL_SQL)
        test_con.commit()
        test_con.close()


def crawl_this_spider(spider_name):
    os.system('cd scp/scrapy_spider && scrapy crawl ' + spider_name)
