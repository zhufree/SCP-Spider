CATE_DB_NAME = 'E:\\SCP-Spider\\scp\\scp_category_v2.db'
DETAIL_DB_NAME = 'E:\\SCP-Spider\\scp\\scp_detail_v2.db'
TEST_DB_NAME = 'E:\\SCP-Spider\\scp\\test_scp.db'
# 先不用这两个字段
# [contest_name] TEXT, 
# [contest_link] TEXT
# [sub_scp_type] TEXT == page_code/event_type/month .etc
# scp表结构
CREATE_DB_SCP_SQL = '''
CREATE TABLE [scps](
  [_id] INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT, 
  [_index] INTEGER NOT NULL,
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [scp_type] INTEGER NOT NULL, 
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

