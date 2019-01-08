# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from .spiders.constants import DB_NAME, DATA_TYPE
from .items import *


def write_to_db(cur, scp_item):
    """
    insert scp_item into db
    """
    try:
        if scp_item['link'] is None:
            scp_item['link'] = ""
        if type(scp_item) == ScpEventItem:
            print("insert ScpEventItem" + scp_item['title'])
            cur.execute('''insert into scps (title, link, scp_type, event_type) values (?,?,?,?)''',
                        (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['event_type'],))
        elif type(scp_item) == ScpTaleItem:
            cur.execute(
                '''insert into scps (title, link, scp_type, author, created_time, month, page_code) values 
                (?,?,?,?,?,?,?)''',
                (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
                 scp_item['created_time'], scp_item['month'], scp_item['page_code'],))
        elif type(scp_item) == ScpStorySeriesItem:
            cur.execute(
                '''insert into scp_collection (title, link, scp_type, author, snippet) values (?,?,?,?,?)''',
                (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
                 scp_item['snippet'],))
        elif type(scp_item) == ScpSettingItem:
            cur.execute('''insert into scps values (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (scp_item['title'], scp_item['link'], scp_item['detail'], scp_item['download_type'],
                         scp_item['scp_type'],
                         scp_item['cn'], scp_item['not_found'], scp_item['author'], scp_item['desc'],
                         scp_item['snippet'],
                         scp_item['subtext'],
                         scp_item['contest_name'], scp_item['contest_link'], scp_item['created_time'],
                         scp_item['month'],
                         scp_item['event_type'], scp_item['page_code'], scp_item['tags'],))
        # elif type(scp_item) == ScpContestWinnerItem:
        #     pass
            # cur.execute(
            #     '''insert into scps (title, link, scp_type, author, contest_name, contest_link) values
            #     (?,?,?,?,?,?)''',
            #     (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
            #      scp_item['contest_name'], scp_item['contest_link'], ))
        elif type(scp_item) == ScpBaseItem:
            print("insert ScpBaseItem" + scp_item['title'])
            cur.execute('''insert into scps (title, link, scp_type) values (?,?,?)''',
                        (scp_item['title'], scp_item['link'], scp_item['scp_type'],))


    except Exception as e:
        print(e)


def update_detail_in_db(cur, detail_item):
    cur.execute('''UPDATE scps SET detail = ?, not_found = ? WHERE LINK = ?''',
                (detail_item['detail'], detail_item['not_found'], detail_item['link']))


class ScpSpiderPipeline(object):

    def open_spider(self, spider):
        self.con = sqlite3.connect(DB_NAME)
        self.cur = self.con.cursor()

    def close_spider(self, spider):
        self.con.commit()
        self.con.close()

    def process_item(self, item, spider):
        print(type(item))
        if type(item) == ScpDetailItem:
            update_detail_in_db(self.cur, item)
        else:
            print("write to db")
            write_to_db(self.cur, item)
        return item

    def parse_detail(self, response):
        detail_dom = response.css('div#page-content')[0]
        print(detail_dom.css('::text')).extract()

    def item_completed(self, results, item, info):
        return item
