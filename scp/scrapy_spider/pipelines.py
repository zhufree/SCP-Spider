# -*- coding: utf-8 -*-
import logging
import sqlite3

from db_constants import ensure_databases
from .items import ScpBaseItem, ScpDetailItem
from .links import normalize_link
from .spiders.constants import CATE_DB_NAME, DETAIL_DB_NAME, TEST_DB_NAME

logger = logging.getLogger(__name__)


def _value(item, key, default=""):
    if key not in item or item[key] is None:
        return default
    return item[key]


def upsert_category(cursor, item):
    link = normalize_link(_value(item, "link"))
    if not link:
        return False
    cursor.execute(
        '''
        INSERT INTO scps (_index, title, link, scp_type, sub_scp_type, author, created_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(link, scp_type) DO UPDATE SET
          _index = excluded._index,
          title = excluded.title,
          sub_scp_type = excluded.sub_scp_type,
          author = CASE
            WHEN excluded.author IS NOT NULL AND excluded.author != '' THEN excluded.author
            ELSE scps.author
          END,
          created_time = CASE
            WHEN excluded.created_time IS NOT NULL AND excluded.created_time != '' THEN excluded.created_time
            ELSE scps.created_time
          END
        ''',
        (
            int(_value(item, "index", 0) or 0),
            _value(item, "title") or link,
            link,
            int(_value(item, "scp_type", 0) or 0),
            _value(item, "sub_scp_type"),
            _value(item, "author"),
            _value(item, "created_time"),
        ),
    )
    return True


def ensure_detail_row(cursor, link):
    cursor.execute("INSERT OR IGNORE INTO scp_detail (link) VALUES (?)", (link,))


def upsert_detail(cursor, item):
    link = normalize_link(_value(item, "link"))
    if not link:
        return False
    cursor.execute(
        '''
        INSERT INTO scp_detail (link, detail, not_found, tags)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(link) DO UPDATE SET
          detail = excluded.detail,
          not_found = excluded.not_found,
          tags = excluded.tags
        ''',
        (
            link,
            _value(item, "detail"),
            int(_value(item, "not_found", 0) or 0),
            _value(item, "tags"),
        ),
    )
    return True


class ScpSpiderPipeline(object):
    def open_spider(self, spider):
        ensure_databases()
        self._pending = 0
        self.cate_con = sqlite3.connect(CATE_DB_NAME)
        self.detail_con = sqlite3.connect(DETAIL_DB_NAME)
        self.test_con = sqlite3.connect(TEST_DB_NAME)
        self.cate_cur = self.cate_con.cursor()
        self.detail_cur = self.detail_con.cursor()
        self.test_cur = self.test_con.cursor()

    def close_spider(self, spider):
        self._commit()
        self.cate_con.close()
        self.detail_con.close()
        self.test_con.close()

    def _commit(self):
        self.cate_con.commit()
        self.detail_con.commit()
        self.test_con.commit()
        self._pending = 0

    def process_item(self, item, spider):
        try:
            if isinstance(item, ScpDetailItem):
                cursor = self.test_cur if spider.name == "test" else self.detail_cur
                upsert_detail(cursor, item)
            elif isinstance(item, ScpBaseItem):
                if spider.name == "test":
                    if upsert_category(self.test_cur, item):
                        ensure_detail_row(self.test_cur, normalize_link(item["link"]))
                else:
                    link = normalize_link(item.get("link"))
                    if upsert_category(self.cate_cur, item):
                        ensure_detail_row(self.detail_cur, link)
            self._pending += 1
            if self._pending >= 50:
                self._commit()
        except Exception:
            logger.exception("failed to write item %s", item.get("link") if hasattr(item, "get") else item)
            raise
        return item
