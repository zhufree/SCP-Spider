DB_NAME = 'E:\\SCP-Spider\\scp\\scp.db'

CREATE_DB_SQL = '''
CREATE TABLE [scps](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [detail] TEXT, 
  [download_type] TEXT, 
  [scp_type] TEXT, 
  [not_found] INTEGER, 
  [author] TEXT, 
  [created_time] TEXT, 
  [month] TEXT, 
  [event_type] TEXT, 
  [page_code] TEXT, 
  [tags] TEXT);
'''

CREATE_COLLECTION_DB_SQL = """

CREATE TABLE [scp_collection](
  [ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [detail] TEXT, 
  [download_type] TEXT, 
  [scp_type] TEXT, 
  [not_found] INTEGER, 
  [desc] TEXT, 
  [snippet] TEXT, 
  [subtext] TEXT, 
  [contest_name] TEXT, 
  [contest_link] TEXT,
  [links] TEXT
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
