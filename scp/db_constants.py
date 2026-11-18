# -*- coding: utf-8 -*-
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

CATE_DB_NAME = str(DATA_DIR / "scp_category_v2.db")
DETAIL_DB_NAME = str(DATA_DIR / "scp_detail_v2.db")
TEST_DB_NAME = str(DATA_DIR / "test_scp.db")

CREATE_DB_SCP_SQL = '''
CREATE TABLE IF NOT EXISTS scps(
  _id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  _index INTEGER NOT NULL,
  title TEXT NOT NULL,
  link TEXT NOT NULL,
  scp_type INTEGER NOT NULL,
  author TEXT,
  created_time TEXT,
  sub_scp_type TEXT);
'''

CREATE_DB_DETAIL_SQL = '''
CREATE TABLE IF NOT EXISTS scp_detail(
  link TEXT PRIMARY KEY UNIQUE NOT NULL,
  not_found INTEGER,
  detail TEXT,
  tags TEXT);
'''


def ensure_databases():
    """Create the data directory, tables, and the category unique key."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_file(CATE_DB_NAME, CREATE_DB_SCP_SQL, with_category_index=True)
    _ensure_file(DETAIL_DB_NAME, CREATE_DB_DETAIL_SQL, with_category_index=False)
    _ensure_file(TEST_DB_NAME, CREATE_DB_SCP_SQL, with_category_index=True)
    _ensure_detail(TEST_DB_NAME)


def _ensure_file(path, create_sql, with_category_index):
    con = sqlite3.connect(path)
    try:
        con.execute(create_sql)
        if with_category_index:
            _ensure_category_unique(con)
        con.commit()
    finally:
        con.close()


def _ensure_detail(path):
    con = sqlite3.connect(path)
    try:
        con.execute(CREATE_DB_DETAIL_SQL)
        con.commit()
    finally:
        con.close()


def _ensure_category_unique(con):
    # Older databases allowed the same link to be inserted on every crawl.
    con.execute(
        '''
        DELETE FROM scps
        WHERE _id NOT IN (
          SELECT MIN(_id) FROM scps GROUP BY link, scp_type
        )
        '''
    )
    con.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_scps_link_type ON scps(link, scp_type)"
    )
