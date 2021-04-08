# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from .spiders.constants import CATE_DB_NAME, DETAIL_DB_NAME, TEST_DB_NAME, DATA_TYPE
from .items import *

need_check_data_type = [DATA_TYPE['reports-interviews-and-logs'], DATA_TYPE['art']]  # 需要去重的type


def check_if_link_exist(cursor, url, scp_type):
    cursor.execute(
        "SELECT * FROM scps WHERE link = '{}' and scp_type = {}".format(
            url, scp_type
        ))
    if cursor.fetchone() is None:
        return False
    else:
        return True


def write_to_db(cate_cur, detail_cur, scp_item):
    """
    insert scp_item into db
    """
    try:
        link = scp_item['link']
        if len(link) == 1 or ('http' in link and 'http://scp-wiki-cn.wikidot.com' not in link):
            return
        else:
            if 'http://scp-wiki-cn.wikidot.com' in link:
                link = link[30:]
            detail_cur.execute('''insert or ignore into scp_detail (link) values (?)''', (link,))
        if type(scp_item) == ScpBaseItem:
            print(scp_item['title'])
            if scp_item['scp_type'] in need_check_data_type:
                if not check_if_link_exist(cate_cur, link, scp_item['scp_type']):
                    cate_cur.execute(
                        '''insert into scps (_index, title, link, scp_type, sub_scp_type) values (?,?,?,?,?)''',
                        (scp_item['index'], scp_item['title'], link, scp_item['scp_type'], scp_item['sub_scp_type'],))
            else:
                cate_cur.execute(
                    '''insert into scps (_index, title, link, scp_type, sub_scp_type) values (?,?,?,?,?)''',
                    (scp_item['index'], scp_item['title'], link, scp_item['scp_type'], scp_item['sub_scp_type'],))
    except Exception as e:
        print(e)


replace_link_dict = {
    '/scp-es-026': '/scp-179',
    '/scp-1001-ru': '/scp-2470',
    '/scp-1047-j': '/joke-scps',
}


def update_detail_in_db(cur, detail_item):
    cur.execute('''INSERT OR REPLACE INTO scp_detail (link, detail, not_found, tags) values (?,?,?,?)''',
                (detail_item['link'], detail_item['detail'], detail_item['not_found'], detail_item['tags'],))


class ScpSpiderPipeline(object):

    def open_spider(self, spider):
        self.cate_con = sqlite3.connect(CATE_DB_NAME)
        self.detail_con = sqlite3.connect(DETAIL_DB_NAME)
        self.test_con = sqlite3.connect(TEST_DB_NAME)
        self.cate_cur = self.cate_con.cursor()
        self.detail_cur = self.detail_con.cursor()
        self.test_cur = self.test_con.cursor()

    def close_spider(self, spider):
        self.cate_con.commit()
        self.detail_con.commit()
        self.test_con.commit()
        self.cate_con.close()
        self.detail_con.close()
        self.test_con.close()

    def process_item(self, item, spider):
        if type(item) == ScpDetailItem:
            update_detail_in_db(self.detail_cur, item)
        else:
            write_to_db(self.cate_cur, self.detail_cur, item)
            # write_to_db(self.test_cur, self.test_cur, item)
        return item

    def item_completed(self, results, item, info):
        return item
