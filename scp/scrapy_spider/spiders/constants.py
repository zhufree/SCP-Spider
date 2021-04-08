HEADERS = {
    'Origin': 'http://scp-wiki-cn.wikidot.com/',
    'Referer': 'http://scp-wiki-cn.wikidot.com/',
    'User-Agent': 'freescp',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

DB_NAME = 'E:\\py-project\\SCP-Spider\\scp\\scp.db'
TEST_DB_NAME = 'E:\\py-project\\SCP-Spider\\scp\\test_scp.db'

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

URL_PARAMS = {
    '_s_': 'http',
    '_d_': 'scp-wiki-cn.wikidot.com',
}

DATA_TYPE = {

    # 系列
    'scp-series': 1,  # 0
    'scp-series-cn': 2,  # 1
    'joke-scps': 3,
    'joke-scps-cn': 4,
    'scp-ex': 5,
    'scp-ex-cn': 6,

    # 故事
    'tales-by-page-name': 7,
    'tales-cn-by-page-name': 8,
    # 设定中心
    'canon-hub': 9,
    'canon-hub-cn': 10,
    # 设定item
    'canon_item': 91,
    # 故事系列
    'series-archive': 11,
    'series-archive-cn': 12,
    'series-archive-item': 111,
    # 事故报告
    'reports-interviews-and-logs': 13,
    'log-of-anomalous-page-cn': 14,

    # 图书馆
    'library-single-page': 17,
    'goi': 18,
    'art': 19,
    # 竞赛
    'contest-archive': 20,
    'contest-archive-item': 201,
    # 中分竞赛
    'contest-archive-cn': 21,
    'contest-archive-cn-item': 211,
    # 放逐者之图书馆
    'wander': 23,
    'wander-cn': 24,
    # 国际版
    'scp-international': 25,

    # 背景和指导
    'info-single-page': 26,

    # 迭代页面
    'offset': 100,

}


# scp系列目录页面
SERIES_ENDPOINTS = [
    '{_s_}://{_d_}/scp-series'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-2'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-3'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-4'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-5'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-6'.format(**URL_PARAMS),
]

# scp-cn系列目录页面
SERIES_CN_ENDPOINTS = [
    '{_s_}://{_d_}/scp-series-cn'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-cn-2'.format(**URL_PARAMS),
    '{_s_}://{_d_}/scp-series-cn-3'.format(**URL_PARAMS),
]

# 图书馆单页
LIBRARY_PAGE_ENDPOINTS = [
    # 用户推荐清单
    '{_s_}://{_d_}/user-curated-lists'.format(**URL_PARAMS),
    # 异常物品记录
    '{_s_}://{_d_}/log-of-anomalous-items'.format(**URL_PARAMS),
    # 超常现象记录
    '{_s_}://{_d_}/log-of-extranormal-events'.format(**URL_PARAMS),
    '{_s_}://{_d_}/log-of-extranormal-events-cn'.format(**URL_PARAMS),
    # 未解明地點記錄
    '{_s_}://{_d_}/log-of-unexplained-locations'.format(**URL_PARAMS),
]

# 异常物品记录-cn, 每个是单页面
CN_ANOMALOUS_PAGE_ENDPOINTS = [
    '{_s_}://{_d_}/log-of-anomalous-items-cn/p/{index}'.format(**URL_PARAMS, index=i) for i in range(1, 8)
]

# 单页面列表，直接抓内容
INFO_PAGE_ENDPOINTS = [
    # 背景资料
    # 安保设施地点
    '{_s_}://{_d_}/secure-facilities-locations'.format(**URL_PARAMS),
    '{_s_}://{_d_}/secure-facilities-locations-cn'.format(**URL_PARAMS),
    # 項目等級
    '{_s_}://{_d_}/object-classes'.format(**URL_PARAMS),
    # 安保许可等级
    '{_s_}://{_d_}/security-clearance-levels'.format(**URL_PARAMS),
    # 机动特遣队
    '{_s_}://{_d_}/task-forces'.format(**URL_PARAMS),

    # 指导
    # 常见问题解答
    '{_s_}://{_d_}/faq'.format(**URL_PARAMS),
    # 给新手的指南
    '{_s_}://{_d_}/guide-for-newbies'.format(**URL_PARAMS),
    # 如何撰写一篇SCP文档
    '{_s_}://{_d_}/how-to-write-an-scp'.format(**URL_PARAMS),
]

# 实验记录3， 探索报告，事故/事件报告，访谈记录，补充材料5，列表
# 要做去重处理
REPORT_ENDPOINTS = [
    '{_s_}://{_d_}/incident-reports-eye-witness-interviews-and-personal-logs/p/{index}'.format(
        **URL_PARAMS, index=i) for i in range(1, 6)
]

# art，列表，要去重
ART_ENDPOINTS = [
    '{_s_}://{_d_}/scp-artwork-hub/p/{index}'.format(**URL_PARAMS, index=i) for i in range(1, 10)
]

# 故事系列列表目录页
SERIES_STORY_ENDPOINTS = [
    '{_s_}://{_d_}/series-archive/p/{index}'.format(**URL_PARAMS, index=i) for i in range(1, 5)
]
CN_SERIES_STORY_ENDPOINTS = [
    '{_s_}://{_d_}/series-archive-cn/p/{index}'.format(**URL_PARAMS, index=i) for i in range(1, 3)
]

# 其他列表页面
ENDPOINTS = {
    # joke
    'joke-scps': '{_s_}://{_d_}/joke-scps'.format(**URL_PARAMS),
    'joke-scps-cn': '{_s_}://{_d_}/joke-scps-cn'.format(**URL_PARAMS),
    # 已解明
    'scp-ex': '{_s_}://{_d_}/scp-ex'.format(**URL_PARAMS),
    'scp-ex-cn': '{_s_}://{_d_}/scp-ex-cn'.format(**URL_PARAMS),

    'tales-by-page-name': '{_s_}://{_d_}/tales-by-page-name'.format(**URL_PARAMS),
    'tales-cn-by-page-name': '{_s_}://{_d_}/tales-cn-by-page-name'.format(**URL_PARAMS),
    # 设定中心
    'canon-hub': '{_s_}://{_d_}/canon-hub'.format(**URL_PARAMS),
    'canon-hub-cn': '{_s_}://{_d_}/canon-hub-cn'.format(**URL_PARAMS),
    # 中国分部故事系列
    'series-archive-cn': '{_s_}://{_d_}/series-archive-cn'.format(**URL_PARAMS),

    # 图书馆
    # GOI
    'goi': '{_s_}://{_d_}/goi-formats'.format(**URL_PARAMS),
    # 征文竞赛
    'contest-archive': '{_s_}://{_d_}/contest-archive'.format(**URL_PARAMS),
    'contest-archive-cn': '{_s_}://{_d_}/contest-archive-cn'.format(**URL_PARAMS),
    # 放逐者图书馆
    'wander': '{_s_}://{_d_}/wanderers:the-index'.format(**URL_PARAMS),
    'wander-cn': '{_s_}://{_d_}/wanderers:the-index-cn'.format(**URL_PARAMS),

    # 国际版
    'scp-international': '{_s_}://{_d_}/scp-international'.format(**URL_PARAMS)
}

LIST_ENDPOINTS = list(ENDPOINTS.values()) + CN_SERIES_STORY_ENDPOINTS + SERIES_STORY_ENDPOINTS + ART_ENDPOINTS + REPORT_ENDPOINTS+\
                 SERIES_CN_ENDPOINTS + SERIES_ENDPOINTS

REVERSE_ENDPOINTS = dict(zip(ENDPOINTS.values(), ENDPOINTS.keys()))



if __name__ == '__main__':
    print(REPORT_ENDPOINTS)