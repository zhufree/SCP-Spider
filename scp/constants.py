DB_NAME = 'E:\\SCP-Spider\\scp\\scp.db'
# 先不用这两个字段
# [contest_name] TEXT, 
# [contest_link] TEXT
# [sub_scp_type] TEXT == page_code/event_type/month .etc
# scp表结构
CREATE_DB_SCP_SQL = '''
CREATE TABLE [scps](
  [_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [_index] INTEGER,
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [download_type] INTEGER, 
  [scp_type] INTEGER, 
  [author] TEXT, 
  [created_time] TEXT, 
  [sub_scp_type] TEXT);
'''

# scp正文内容表结构，用link检索
CREATE_DB_DETAIL_SQL = '''
CREATE TABLE [scp_detail](
  [link] TEXT PRIMARY KEY UNIQUE, 
  [not_found] INTEGER, 
  [detail] TEXT, 
  [tags] TEXT);
'''


CREATE_COLLECTION_DB_SQL = """
CREATE TABLE [scp_collection](
  [_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [_index] INTEGER,
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [download_type] INTEGER, 
  [scp_type] INTEGER, 
  [author] TEXT,
  [desc] TEXT, 
  [creator] TEXT,
  [snippet] TEXT, 
  [subtext] TEXT, 
  [sub_links] TEXT
);
"""

CREATE_TAG_DB_SQL = """
CREATE TABLE [tag_scp](
  [_id] INTEGER PRIMARY KEY, 
  [link] TEXT UNIQUE, 
  [title] TEXT, 
  [detail] TEXT, 
  [tags] TEXT);
"""
