HEADERS = {
    'Origin': 'http://scp-wiki-cn.wikidot.com/',
    'Referer': 'http://scp-wiki-cn.wikidot.com/',
    'User-Agent': 'freescp',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

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

URL_PARAMS = {
    '_s_': 'http',
    '_d_': 'scp-wiki-cn.wikidot.com',
}

DATA_TYPE = {
    # 3
    'single-page': 0,

    'scp-series': 1,  # 0
    'scp-series-cn': 2,  # 1
    # 2
    'tales-by-page-name': 3,
    'tales-cn-by-page-name': 4,
    # 3
    'joke-scps': 5,
    'joke-scps-cn': 6,
    'archived-scps': 7,
    'scp-ex': 8,
    'scp-ex-cn': 9,
    'decommissioned-scps': 10,
    'scp-removed': 11,
    'reports-interviews-and-logs': 12,
    # 4
    'canon-hub': 13,
    'canon-hub-cn': 14,
    'contest-archive': 15,
    'contest-archive-winner': 16,
    'contest-archive-cn': 17,
    'contest-archive-cn-winner': 18,
    'series-archive': 19,
    'series-archive-cn': 20,
    'offset': 21
}

TALE_LETTER_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']
SERIES_ENDPOINTS = [
    '{_s_}://{_d_}/scp-series'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-2'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-3'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-4'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-5'.format(**URL_PARAMS),
]

SERIES_CN_ENDPOINTS = [
    '{_s_}://{_d_}/scp-series-cn'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-cn-2'.format(**URL_PARAMS),
]

SINGLE_PAGE_ENDPOINTS = [
    '{_s_}://{_d_}/secure-facilities-locations'.format(**URL_PARAMS),
    '{_s_}://{_d_}/secure-facilities-locations-cn'.format(**URL_PARAMS),
    '{_s_}://{_d_}/object-classes'.format(**URL_PARAMS),
    '{_s_}://{_d_}/security-clearance-levels'.format(**URL_PARAMS),
    '{_s_}://{_d_}/task-forces'.format(**URL_PARAMS),

    '{_s_}://{_d_}/log-of-extranormal-events'.format(**URL_PARAMS),
    '{_s_}://{_d_}/log-of-extranormal-events-cn'.format(**URL_PARAMS),
    '{_s_}://{_d_}/log-of-anomalous-items'.format(**URL_PARAMS),
    '{_s_}://{_d_}/log-of-anomalous-items-cn'.format(**URL_PARAMS),

    '{_s_}://{_d_}/faq'.format(**URL_PARAMS),
    '{_s_}://{_d_}/guide-for-newbies'.format(**URL_PARAMS),
    '{_s_}://{_d_}/how-to-write-an-scp'.format(**URL_PARAMS),
]

REPORT_ENDPOINTS = [
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/1'.format(
        **URL_PARAMS),
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/2'.format(
        **URL_PARAMS),
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/3'.format(
        **URL_PARAMS),
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/4'.format(
        **URL_PARAMS),
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/5'.format(
        **URL_PARAMS)
]

ENDPOINTS = {
    # list
    'tales-by-page-name': '{_s_}://{_d_}/tales-by-page-name'.format(**URL_PARAMS),
    'tales-cn-by-page-name': '{_s_}://{_d_}/tales-cn-by-page-name'.format(**URL_PARAMS),
    'joke-scps': '{_s_}://{_d_}/joke-scps'.format(**URL_PARAMS),
    'joke-scps-cn': '{_s_}://{_d_}/joke-scps-cn'.format(**URL_PARAMS),
    'archived-scps': '{_s_}://{_d_}/archived-scps'.format(**URL_PARAMS),
    'scp-ex': '{_s_}://{_d_}/scp-ex'.format(**URL_PARAMS),
    'scp-ex-cn': '{_s_}://{_d_}/scp-ex-cn'.format(**URL_PARAMS),
    'decommissioned-scps': '{_s_}://{_d_}/decommissioned-scps-arc'.format(**URL_PARAMS),
    'scp-removed': '{_s_}://{_d_}/scp-removed'.format(**URL_PARAMS),

    # TODO 竞赛改成抓竞赛主页
}

REVERSE_ENDPOINTS = dict(zip(ENDPOINTS.values(), ENDPOINTS.keys()))

SERIES_STORY_ENDPOINTS = [
    '{_s_}://{_d_}/series-archive'.format(**URL_PARAMS),
    '{_s_}://{_d_}/series-archive/p/2'.format(**URL_PARAMS),
    '{_s_}://{_d_}/series-archive/p/3'.format(**URL_PARAMS),
    '{_s_}://{_d_}/series-archive/p/4'.format(**URL_PARAMS),
]

COLLECTION_ENDPOINTS = {
    'canon-hub': '{_s_}://{_d_}/canon-hub'.format(**URL_PARAMS),
    'canon-hub-cn': '{_s_}://{_d_}/canon-hub-cn'.format(**URL_PARAMS),
    'contest-archive': '{_s_}://{_d_}/contest-archive'.format(**URL_PARAMS),
    'contest-archive-cn': '{_s_}://{_d_}/contest-archive-cn'.format(**URL_PARAMS),
    'series-archive-cn': '{_s_}://{_d_}/series-archive-cn'.format(**URL_PARAMS),
}

REVERSE_COLLECTION_ENDPOINTS = dict(zip(COLLECTION_ENDPOINTS.values(), COLLECTION_ENDPOINTS.keys()))
