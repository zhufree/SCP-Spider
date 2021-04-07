from pyquery import PyQuery as pq
from .constants import DATA_TYPE, HEADERS, SERIES_ENDPOINTS, SERIES_CN_ENDPOINTS, LIBRARY_PAGE_ENDPOINTS, ENDPOINTS, \
    REVERSE_ENDPOINTS, INFO_PAGE_ENDPOINTS, SERIES_STORY_ENDPOINTS, REPORT_ENDPOINTS, DB_NAME, URL_PARAMS, \
    CN_ANOMALOUS_ITEM_ENDPOINTS, ART_ENDPOINTS
from ..items import *
from .parse import parse_html
import sqlite3


# 根据url反向获取scp_type
def get_type_by_url(url):
    if url in SERIES_ENDPOINTS:
        return DATA_TYPE['scp-series']
    elif url in SERIES_CN_ENDPOINTS:
        return DATA_TYPE['scp-series-cn']
    elif url in SERIES_STORY_ENDPOINTS:
        return DATA_TYPE['series-archive']
    elif url in LIBRARY_PAGE_ENDPOINTS:
        return DATA_TYPE['library-single-page']
    elif url in REPORT_ENDPOINTS:
        return DATA_TYPE['reports-interviews-and-logs']
    elif url in CN_ANOMALOUS_ITEM_ENDPOINTS:
        return DATA_TYPE['log-of-anomalous-items-cn']
    elif url in ART_ENDPOINTS:
        return DATA_TYPE['art']
    elif url in INFO_PAGE_ENDPOINTS:
        return DATA_TYPE['info-single-page']
    elif url in ENDPOINTS.values():
        return DATA_TYPE[REVERSE_ENDPOINTS[url]]
    else:
        return -1


# 获取detail表中内容为空的link
def get_empty_link_for_detail():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scp_detail where detail is NULL;')
    link_list = [t[0] for t in cur if 'http' not in t]
    con.close()
    return link_list


# 获取detail表中404的link
def get_404_link_for_detail():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scp_detail where not_found = 1;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list


# 根据download_type获取所有link
def get_all_link():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scps;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list
    # return ['/scp-cn-1000']


def get_collection_item_link():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scp_collection;')
    link_list = [t[0] for t in cur if 'forum' not in t] + ['/scp-001']
    con.close()
    return link_list


class ScpListSpider(scrapy.Spider):
    """
    抓取scp列表
    """
    name = "main"
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    # 页面不多可以一次抓完
    # SERIES_ENDPOINTS # 6
    # SERIES_CN_ENDPOINTS # 3
    item_list_urls = list(ENDPOINTS.values()) + REPORT_ENDPOINTS
    collection_list_url = list(COLLECTION_ENDPOINTS.values()) + SERIES_STORY_ENDPOINTS

    start_urls = SERIES_CN_ENDPOINTS + SERIES_ENDPOINTS
                 # + item_list_urls + collection_list_url

    # start_urls = [ENDPOINTS['scp-ex-cn']]  # 漏抓补充

    def parse(self, response):
        pq_doc = pq(response.body)
        item_list = parse_html(pq_doc, get_type_by_url(response.url))
        for info in item_list:
            yield info


# 在main里面抓
# class ScpInternationalSpider(scrapy.Spider):
#     """
#     抓取scp列表
#     """
#     name = "international"
#     allowed_domains = 'scp-wiki-cn.wikidot.com'
#
#     start_urls = [ENDPOINTS['scp-international']]
#
#
#     def parse(self, response):
#         pq_doc = pq(response.body)
#         item_list = parse_html(pq_doc, get_type_by_url(response.url))
#         for info in item_list:
#             yield info


class ScpTestSpider(scrapy.Spider):
    """
    抓取scp列表
    """
    name = "test"
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    # start_urls = [SERIES_ENDPOINTS[5]]
    start_urls = ['http://scp-wiki-cn.wikidot.com/contest-archive']

    def parse(self, response):
        pq_doc = pq(response.body)
        item_list = parse_html(pq_doc, get_type_by_url(response.url))
        for info in item_list:
            yield info


class ScpSinglePageSpider(scrapy.Spider):
    """
    抓取单页面
    """
    name = "single"
    allowed_domains = 'scp-wiki-cn.wikidot.com'
    start_urls = INFO_PAGE_ENDPOINTS
    index = 0

    def parse(self, response):
        pq_doc = pq(response.body)
        new_scp = ScpBaseItem(index=self.index, link=response.url[30:], title=pq_doc('div#page-title').text(),
                              scp_type=DATA_TYPE['single-page'], sub_scp_type='')
        self.index += 1
        yield new_scp


class ScpDetailSpider(scrapy.Spider):
    """
    根据链接抓取页面内容
    """
    name = 'detail'
    allowed_domains = 'scp-wiki-cn.wikidot.com'
    start_urls = [('{_s_}://{_d_}' + link).format(**URL_PARAMS) for link in get_empty_link_for_detail()]
    handle_httpstatus_list = [404]  # 处理404页面，否则将会跳过

    def parse(self, response):
        if response.status != 404:
            detail_dom = response.css('div#page-content')[0]
            link = response.url[30:]
            extra_detail_item = None
            if link == '/taboo':
                link = '/scp-4000'
            if link == '/numbered':
                link = '/scp-cn-1100'
            if link == '/scp-179/':
                extra_detail_item = ScpDetailItem(link='/scp-es-026',
                                                  detail=detail_dom.extract().replace('  ', '').replace('\n', ''),
                                                  not_found=0)
            if link == '/scp-2522':
                extra_detail_item = ScpDetailItem(link='/SCP-2522',
                                                  detail=detail_dom.extract().replace('  ', '').replace('\n', ''),
                                                  not_found=0)
            detail_item = ScpDetailItem(link=link,
                                        detail=detail_dom.extract().replace('  ', '').replace('\n', ''), not_found=0)
            if extra_detail_item is not None:
                yield extra_detail_item
        else:
            detail_item = ScpDetailItem(link=response.url[30:], detail="null", not_found=1)
        yield detail_item


class ScpOffsetSpider(scrapy.Spider):
    """
    抓offset内容
    """
    name = 'offset'
    allowed_domains = 'scp-wiki-cn.wikidot.com'
    # 根据download_type分一下
    start_urls = [('{_s_}://{_d_}' + link + '/offset/1').format(**URL_PARAMS) for link in
                  get_all_link()]
    handle_httpstatus_list = [404]  # 处理404页面，否则将会跳过

    def parse(self, response):
        dom = pq(response.body)
        if response.status != 404 and len(list(dom.find('#page-content .list-pages-box .list-pages-item'))) > 0:
            detail_dom = response.css('div#page-content')[0]
            offset_index = int(response.url.split('/')[-1])  # .../scp-xxx/offset/x
            link = response.url[30:]
            detail_item = ScpDetailItem(link=link, detail=detail_dom.extract().replace('  ', '').replace('\n', ''),
                                        not_found=0)
            yield detail_item
            offset_request = scrapy.Request(response.url[0:-1] + str(offset_index + 1), callback=parse_offset,
                                            headers=HEADERS, dont_filter=True)
            yield offset_request
        # yield detail_item


def parse_offset(response):
    if response.status != 404 and len(response.css('#page-content .list-pages-box.list-page-item')) > 0:
        # offset为空不是404，需要判断这个标签内容是不是为空
        detail_dom = response.css('div#main-content')[0]
        offset_index = int(response.url.split('/')[-1])  # .../scp-xxx/offset/x
        link = response.url[30:]
        title = response.css('div#page-title')[0].css('::text').extract()[0].strip() + '-offset-' + str(offset_index)
        offset_item = ScpBaseItem(index=0, link=link, title=title, scp_type=DATA_TYPE['offset'])
        detail_item = ScpDetailItem(link=link, detail=detail_dom.extract().replace('  ', '').replace('\n', ''),
                                    not_found=0)
        yield offset_item
        yield detail_item
        offset_request = scrapy.Request(response.url[0:-1] + str(offset_index + 1), callback=parse_offset,
                                        headers=HEADERS, dont_filter=True)
        yield offset_request


# 抓设定中心/竞赛内容/故事系列页里面的列表
class ScpCollectionSpider(scrapy.Spider):
    name = "collection_list"
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    start_urls = list(set([('{_s_}://{_d_}' + link).format(**URL_PARAMS) for link in
                           get_collection_item_link()]))
    handle_httpstatus_list = [404]  # 处理404页面，否则将会跳过

    def __init__(self, category=None, *args, **kwargs):
        super(ScpCollectionSpider, self).__init__(*args, **kwargs)
        self.con = sqlite3.connect(DB_NAME)
        self.cur = self.con.cursor()

    def close(self, reason):
        super(ScpCollectionSpider, self).close(self, reason=reason)
        self.con.close()

    def parse(self, response):
        pq_doc = pq(response.body)
        scp_type = self.get_type_by_url(response.url[30:])
        if scp_type == 13 or scp_type == 14 or scp_type == 1:  # '/scp-001'
            sub_item_type = 22
        elif scp_type == 19 or scp_type == 20:
            sub_item_type = 23
        else:
            sub_item_type = scp_type + 1
        item_list = parse_html(pq_doc, sub_item_type)
        for info in item_list:
            yield info

    def get_type_by_url(self, link):
        if link == '/scp-001':
            return 1
        self.cur.execute('''select scp_type from scp_collection where link = ?''', (link,))
        scp_type = [t[0] for t in self.cur][0]
        return scp_type


class ScpTagSpider(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "tag_spider"  # 定义蜘蛛名
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    start_urls = [
        # tag
        'http://scp-wiki-cn.wikidot.com/system:page-tags/',
    ]

    def parse(self, response):
        pq_doc = pq(response.body)
        for a in pq_doc('div.pages-tag-cloud-box a').items():
            tag_name = a.text()
            link = a.attr('href')
            tag_request = scrapy.Request(response.urljoin(link), callback=parse_tag, headers=HEADERS)
            tag_request.meta['tag_name'] = tag_name
            yield tag_request


def parse_tag(response):
    pq_doc = pq(response.body)
    tag_name = response.meta['tag_name']
    for article_div in pq_doc('div#tagged-pages-list div.pages-list-item').items():
        new_article = ScpTagItem(
            title=article_div.text(),
            link=article_div('a').attr('href'),
            tags=tag_name,
        )
        yield new_article
