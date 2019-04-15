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
        else:
            cur.execute('''insert or ignore into scp_detail (link) values (?)''', (scp_item['link'],))
        # if type(scp_item) == ScpEventItem:
        #     print("insert ScpEventItem" + scp_item['title'])
        #     cur.execute('''insert into scps (title, link, scp_type, event_type) values (?,?,?,?)''',
        #                 (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['event_type'],))
        if type(scp_item) == ScpTaleItem:
            cur.execute(
                '''insert into scps (_index, title, link, scp_type, author, created_time, sub_scp_type) values 
                (?,?,?,?,?,?,?)''',
                (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
                 scp_item['created_time'], scp_item['sub_scp_type'],))
        elif type(scp_item) == ScpStorySeriesItem:
            print("insert ScpStorySeriesItem")
            cur.execute(
                '''insert into scp_collection (_index, title, link, scp_type, author, snippet) values (?,?,?,?,?,?)''',
                (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
                 scp_item['snippet'],))
        elif type(scp_item) == ScpContestArticleItem:
            print("insert ScpContestArticleItem")
            cur.execute(
                '''insert into scps (_index, title, link, scp_type) values
                    (?,?,?,?)''',
                (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type']))
        elif type(scp_item) == ScpContestItem:
            print("insert ScpContestItem")
            cur.execute(
                '''insert into scp_collection (_index, title, link, scp_type, author) values 
                    (?,?,?,?,?)''',
                (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['creator'],))
        elif type(scp_item) == ScpSettingItem:
            print("insert ScpSettingItem")
            cur.execute('''insert into scp_collection (_index, title, link, scp_type, desc, snippet, subtext) values 
                (?,?,?,?,?,?,?)''',
                        (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['desc'],
                         scp_item['snippet'], scp_item['subtext'],))
        elif type(scp_item) == ScpBaseItem:
            print(scp_item['title'])
            if scp_item['scp_type'] == DATA_TYPE['offset']:
                print("insert ScpOffsetItem" + scp_item['title'])
                cur.execute('''insert or replace into scp_detail (link, detail, not_found) values (?,?,?)''',
                            (scp_item['link'], scp_item['detail'], scp_item['not_found'],))
            else:
                cur.execute('''insert into scps (_index, title, link, scp_type) values (?,?,?,?)''',
                            (scp_item['index'], scp_item['title'], scp_item['link'], scp_item['scp_type'],))

    except Exception as e:
        print(e)


def update_detail_in_db(cur, detail_item):
    cur.execute('''UPDATE scp_detail SET detail = ?, not_found = ? WHERE LINK = ?''',
                (detail_item['detail'], detail_item['not_found'], detail_item['link']))
    # cur.execute('''UPDATE scp_collection SET detail = ?, not_found = ? WHERE LINK = ?''',
    #             (detail_item['detail'], detail_item['not_found'], detail_item['link']))


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
