DB_NAME = 'E:\\SCP-Spider\\scp\\scp.db'

CREATE_DB_SQL = '''
CREATE TABLE [scps](
  [_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [detail] TEXT, 
  [download_type] INTEGER, 
  [scp_type] INTEGER, 
  [not_found] INTEGER, 
  [author] TEXT, 
  [created_time] TEXT, 
  [month] TEXT, 
  [event_type] TEXT, 
  [page_code] TEXT, 
  [contest_name] TEXT, 
  [contest_link] TEXT,
  [tags] TEXT);
'''

CREATE_COLLECTION_DB_SQL = """

CREATE TABLE [scp_collection](
  [_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
  [title] TEXT NOT NULL, 
  [link] TEXT NOT NULL, 
  [detail] TEXT, 
  [download_type] INTEGER, 
  [scp_type] INTEGER, 
  [not_found] INTEGER, 
  [author] TEXT,
  [desc] TEXT, 
  [creator] TEXT,
  [snippet] TEXT, 
  [subtext] TEXT, 
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