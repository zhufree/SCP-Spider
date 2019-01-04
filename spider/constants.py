HEADERS = {
    'Origin': 'http://scp-wiki-cn.wikidot.com/',
    'Referer': 'http://scp-wiki-cn.wikidot.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '68.0.3440.106 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

DB_NAME = 'scp.db'

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

CREATE TABLE [tag_scp](
  [_id] INTEGER PRIMARY KEY, 
  [link] TEXT UNIQUE, 
  [title] TEXT, 
  [detail] TEXT, 
  [tags] TEXT);

'''

_url_params_ = {
    '_s_': 'http',
    '_d_': 'scp-wiki-cn.wikidot.com',
}

DATA_TYPE = {
    # list
    'scp-series': 0,
    'scp-series-cn': 1,
    'foundation-tales': 2,
    'foundation-tales-cn': 3,
    'joke-scps': 4,
    'joke-scps-cn': 5,
    'archived-scps': 6,
    'scp-ex': 7,
    'scp-ex-cn': 8,
}

ENDPOINTS = {
    # list
    'scp-series': '{_s_}://{_d_}/scp-series'.format(**_url_params_),
    'scp-series-cn': '{_s_}://{_d_}/scp-series-cn'.format(**_url_params_),
    'foundation-tales': '{_s_}://{_d_}/foundation-tales'.format(**_url_params_),
    'foundation-tales-cn': '{_s_}://{_d_}/foundation-tales-cn'.format(**_url_params_),
    'joke-scps': '{_s_}://{_d_}/joke-scps'.format(**_url_params_),
    'joke-scps-cn': '{_s_}://{_d_}/joke-scps-cn'.format(**_url_params_),
    'archived-scps': '{_s_}://{_d_}/archived-scps'.format(**_url_params_),
    'scp-ex': '{_s_}://{_d_}/scp-ex'.format(**_url_params_),
    'scp-ex-cn': '{_s_}://{_d_}/scp-ex-cn'.format(**_url_params_),
    'reports-interviews-and-logs': '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs'.format(
        **_url_params_),
    # single page
    'secure-facilities-locations': '{_s_}://{_d_}/secure-facilities-locations'.format(**_url_params_),
    'secure-facilities-locations-cn': '{_s_}://{_d_}/secure-facilities-locations-cn'.format(**_url_params_),
    'object-classes': '{_s_}://{_d_}/object-classes'.format(**_url_params_),
    'security-clearance-levels': '{_s_}://{_d_}/security-clearance-levels'.format(**_url_params_),
    'log-of-extranormal-events': '{_s_}://{_d_}/log-of-extranormal-events'.format(**_url_params_),
    'log-of-extranormal-events-cn': '{_s_}://{_d_}/log-of-extranormal-events-cn'.format(**_url_params_),
    'log-of-anomalous-items': '{_s_}://{_d_}/log-of-anomalous-items'.format(**_url_params_),
    'log-of-anomalous-items-cn': '{_s_}://{_d_}/log-of-anomalous-items-cn'.format(**_url_params_),
    'task-forces': '{_s_}://{_d_}/task-forces'.format(**_url_params_),

    'faq': '{_s_}://{_d_}/faq'.format(**_url_params_),
    'guide-for-newbies': '{_s_}://{_d_}/guide-for-newbies'.format(**_url_params_),
    'how-to-write-an-scp': '{_s_}://{_d_}/how-to-write-an-scp'.format(**_url_params_),
}
