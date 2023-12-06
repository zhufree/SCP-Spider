HEADERS = {
    'Origin': 'http://scp-wiki-cn.wikidot.com/',
    'Referer': 'http://scp-wiki-cn.wikidot.com/',
    'User-Agent': 'freescp',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
base_dir = 'E:\\SCP-Spider\\'
CATE_DB_NAME = base_dir + 'scp_category_v2.db'
DETAIL_DB_NAME = base_dir + 'scp_detail_v2.db'
TEST_DB_NAME = base_dir + 'test_scp.db'

# 先不用这两个字段
# [contest_name] TEXT, 
# [contest_link] TEXT
# [sub_scp_type] TEXT == page_code/event_type/month .etc
# scp表结构
CREATE_DB_SCP_SQL = '''
CREATE TABLE [scps](
  [_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
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

URL_BASE = 'https://scp-wiki-cn.wikidot.com'

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
    # 故事系列
    'series-archive': 11,
    'series-archive-cn': 12,
    # 事故报告
    'reports-interviews-and-logs': 13,
    'log-of-anomalous-page-cn': 14,
    'short-story': 15,

    # 图书馆
    'library-single-page': 16,
    'goi': 17,
    'art': 18,
    # 竞赛
    'contest-archive': 19,
    # 中分竞赛
    'contest-archive-cn': 20,
    # 放逐者之图书馆
    'wander': 21,
    'wander-cn': 22,
    # 国际版
    'scp-international': 23,

    # 背景和指导
    'info-single-page': 24,

    # 迭代页面
    'offset': 100,
}


# scp系列目录页面
SERIES_ENDPOINTS = [
    f'{URL_BASE}/scp-series',
    f'{URL_BASE}/scp-series-2',
    f'{URL_BASE}/scp-series-3',
    f'{URL_BASE}/scp-series-4',
    f'{URL_BASE}/scp-series-5',
    f'{URL_BASE}/scp-series-6',
    f'{URL_BASE}/scp-series-7',
    f'{URL_BASE}/scp-series-8',
]

# scp-cn系列目录页面
SERIES_CN_ENDPOINTS = [
    f'{URL_BASE}/scp-series-cn',
    f'{URL_BASE}/scp-series-cn-2',
    f'{URL_BASE}/scp-series-cn-3',
]

# 图书馆单页
LIBRARY_PAGE = [
    # 用户推荐清单
    f'{URL_BASE}/user-curated-lists',
    # 异常物品记录
    f'{URL_BASE}/log-of-anomalous-items',
    # 超常现象记录
    f'{URL_BASE}/log-of-extranormal-events',
    f'{URL_BASE}/log-of-extranormal-events-cn',
    # 未解明地點記錄
    f'{URL_BASE}/log-of-unexplained-locations',
]

# 异常物品记录-cn, 每个是单页面
CN_ANOMALOUS_PAGE = [
    f'{URL_BASE}/log-of-anomalous-items-cn/p/{index}' for index in range(1, 8)
]

SHORT_STORY_PAGE = [
    f'{URL_BASE}/short-stories/p/{index}' for index in range(1, 4)
]

# 单页面列表，直接抓内容
INFO_PAGE = [
    # 背景资料
    # 关于基金会
    f'{URL_BASE}/about-the-scp-foundation',
    # 相关组织
    f'{URL_BASE}/groups-of-interest',
    f'{URL_BASE}/groups-of-interest-cn',
    # 項目等級
    f'{URL_BASE}/object-classes',
    # 人员及角色档案
    f'{URL_BASE}/personnel-and-character-dossier',
    # 安保许可等级
    f'{URL_BASE}/security-clearance-levels',
    # 安保设施地点
    f'{URL_BASE}/secure-facilities-locations',
    f'{URL_BASE}/secure-facilities-locations-cn',
    # 机动特遣队
    f'{URL_BASE}/task-forces',

    # 指导
    # 指导中心
    f'{URL_BASE}/guide-hub',
    # 常见问题解答
    f'{URL_BASE}/faq',
    # 给新手的指南
    f'{URL_BASE}/guide-for-newbies',
    # 如何撰写一篇SCP文档
    f'{URL_BASE}/how-to-write-an-scp',
    # 图像使用原则
    f'{URL_BASE}/image-use-policy',
    # 授权指南
    f'{URL_BASE}/licensing-guide',
    # 标签指导
    f'{URL_BASE}/tag-guide',
    # 已翻译文档發佈及搬运指南
    f'{URL_BASE}/translation-movement-guide',
    # SCP-CN翻译发布与校对规范
    f'{URL_BASE}/translation-rules',
    # 站规
    f'{URL_BASE}/site-rules',
    # 删帖指导
    f'{URL_BASE}/deletions-guide',
    # 批評守則
    f'{URL_BASE}/criticism-policy',
]

# 实验记录3， 探索报告，事故/事件报告，访谈记录，补充材料5，列表
# 要做去重处理
REPORT_ENDPOINTS = [
    f'{URL_BASE}/incident-reports-eye-witness-interviews-and-personal-logs/p/{index}' for index in range(1, 6)
]

# art，列表，要去重
ART_ENDPOINTS = [
    f'{URL_BASE}/scp-artwork-hub/p/{index}' for index in range(1, 10)
]

# 故事系列列表目录页
SERIES_STORY_ENDPOINTS = [
    f'{URL_BASE}/series-archive/p/{index}' for index in range(1, 5)
]
CN_SERIES_STORY_ENDPOINTS = [
    f'{URL_BASE}/series-archive-cn/p/{index}' for index in range(1, 3)
]

# 其他列表页面
ENDPOINTS = {
    # joke
    'joke-scps': f'{URL_BASE}/joke-scps',
    'joke-scps-cn': f'{URL_BASE}/joke-scps-cn',
    # 已解明
    'scp-ex': f'{URL_BASE}/scp-ex',
    'scp-ex-cn': f'{URL_BASE}/scp-ex-cn',

    'tales-by-page-name': f'{URL_BASE}/tales-by-page-name',
    'tales-cn-by-page-name': f'{URL_BASE}/tales-cn-by-page-name',
    # 设定中心
    'canon-hub': f'{URL_BASE}/canon-hub',
    'canon-hub-cn': f'{URL_BASE}/canon-hub-cn',
    # 中国分部故事系列
    'series-archive-cn': f'{URL_BASE}/series-archive-cn',

    # 图书馆
    # GOI
    'goi': f'{URL_BASE}/goi-formats',
    # 征文竞赛
    'contest-archive': f'{URL_BASE}/contest-archive',
    'contest-archive-cn': f'{URL_BASE}/contest-archive-cn',
    # 放逐者图书馆
    'wander': f'{URL_BASE}/wanderers:the-index',
    'wander-cn': f'{URL_BASE}/wanderers:the-index-cn',

    # 国际版
    'scp-international': f'{URL_BASE}/scp-international'
}

LIST_ENDPOINTS = list(ENDPOINTS.values()) + ART_ENDPOINTS + REPORT_ENDPOINTS \
    + SERIES_STORY_ENDPOINTS + CN_SERIES_STORY_ENDPOINTS \
    + SERIES_CN_ENDPOINTS + SERIES_ENDPOINTS

REVERSE_ENDPOINTS = dict(zip(ENDPOINTS.values(), ENDPOINTS.keys()))


if __name__ == '__main__':
    print(REPORT_ENDPOINTS)