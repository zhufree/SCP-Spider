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
    :return:
    """
    try:
        if type(scp_item) == ScpBaseItem:
            cur.execute('''insert into scps (title, link, scp_type) values (?,?,?)''',
                        (scp_item['title'], scp_item['link'], scp_item['scp_type'],))
        elif type(scp_item) == ScpTaleItem:
            cur.execute(
                '''insert into scps (title, link, scp_type, author, created_time, month, page_code) values (?,?,?)''',
                (scp_item['title'], scp_item['link'], scp_item['scp_type'], scp_item['author'],
                 scp_item['created_time'], scp_item['month'], scp_item['page_code'],))
        elif type(scp_item) == ScpStorySeriesItem:
            pass
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
        elif type(scp_item) == ScpContestItem:
            pass
        elif type(scp_item) == ScpEventItem:
            pass

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
        if type(item) == ScpDetailItem:
            update_detail_in_db(self.cur, item)
        else:
            write_to_db(self.cur, item)
        return item

    def parse_detail(self, response):
        detail_dom = response.css('div#page-content')[0]
        # for category in total_scps_list:
        #     if category['link'] == link:
        #         category['not_found'] = "false"
        #         category['detail'] = detail_dom.html().replace('  ', '').replace('\n', '')
        print(detail_dom.css('::text')).extract()
        # a_in_detail = detail_dom.remove('.footer-wikiwalk-nav')('a')
        # if len(list(a_in_detail.items())) > 30:
        #     return
        # for a in a_in_detail.items():
        #     href = a.attr('href')
        #     if href.startswith('/') and href not in total_link_list:
        #         print('new link = ' + href)
        #         new_link.append(href)
        #         new_found_link_list.append(href)
        #         title = a.text()
        #         new_category = {
        #             'title': title,
        #             'link': href,
        #             'type': 'none'
        #         }
        #         new_found_category_list.append(new_category)

    def item_completed(self, results, item, info):
        return item
