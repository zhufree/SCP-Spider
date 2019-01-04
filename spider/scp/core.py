# -*- coding: utf-8 -*-

from ..constants import DB_NAME, CREATE_DB_SQL
import sqlite3
import os


def init_database():
    if not os.path.exists(DB_NAME):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute(CREATE_DB_SQL)
        con.commit()
        con.close()


class ScpSpider:
    def __init__(self) -> None:
        # init database file
        init_database()

    def crawl_main_list(self):
        # use scrapy crawl scp list and save in db
        pass
