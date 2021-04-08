from pyquery import PyQuery as pq
from .constants import DATA_TYPE, HEADERS, SERIES_ENDPOINTS, SERIES_CN_ENDPOINTS, LIBRARY_PAGE, ENDPOINTS, \
    REVERSE_ENDPOINTS, INFO_PAGE, SERIES_STORY_ENDPOINTS, REPORT_ENDPOINTS, CATE_DB_NAME, DETAIL_DB_NAME, \
    URL_PARAMS, CN_ANOMALOUS_PAGE, ART_ENDPOINTS, CN_SERIES_STORY_ENDPOINTS, LIST_ENDPOINTS, SHORT_STORY_PAGE
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
    elif url in CN_SERIES_STORY_ENDPOINTS:
        return DATA_TYPE['series-archive-cn']
    elif url in LIBRARY_PAGE:
        return DATA_TYPE['library-single-page']
    elif url in REPORT_ENDPOINTS:
        return DATA_TYPE['reports-interviews-and-logs']
    elif url in CN_ANOMALOUS_PAGE:
        return DATA_TYPE['log-of-anomalous-page-cn']
    elif url in ART_ENDPOINTS:
        return DATA_TYPE['art']
    elif url in INFO_PAGE:
        return DATA_TYPE['info-single-page']
    elif url in SHORT_STORY_PAGE:
        return DATA_TYPE['short-story']
    elif url in ENDPOINTS.values():
        return DATA_TYPE[REVERSE_ENDPOINTS[url]]
    else:
        return -1


# 获取detail表中内容为空的link
def get_empty_link_for_detail():
    con = sqlite3.connect(DETAIL_DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scp_detail where detail is NULL;')
    link_list = [t[0] for t in cur if 'http' not in t]
    con.close()
    return link_list


# 获取detail表中404的link
def get_404_link_for_detail():
    con = sqlite3.connect(DETAIL_DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scp_detail where not_found = 1;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list


# 根据download_type获取所有link
def get_all_link():
    con = sqlite3.connect(CATE_DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scps;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list
    # return ['/scp-cn-1000']


class ScpTestSpider(scrapy.Spider):
    """
    测试用
    """
    name = "test"
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    start_urls = [ENDPOINTS['scp-international']]

    def parse(self, response):
        pq_doc = pq(response.body)
        item_list = parse_html(pq_doc, get_type_by_url(response.url))
        for info in item_list:
            yield info


class ScpListSpider(scrapy.Spider):
    """
    抓取scp列表
    """
    name = "main"
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    # 页面不多可以一次抓完
    start_urls = LIST_ENDPOINTS

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
    start_urls = LIBRARY_PAGE + INFO_PAGE + CN_ANOMALOUS_PAGE + SHORT_STORY_PAGE
    index = 0

    def parse(self, response):
        pq_doc = pq(response.body)
        if response.url in SHORT_STORY_PAGE or response.url in CN_ANOMALOUS_PAGE:
            title = pq_doc('div#page-title').text() + response.url.split('/')[-1]
        else:
            title = pq_doc('div#page-title').text()
        new_scp = ScpBaseItem(index=self.index, link=response.url[30:], title=title,
                              scp_type=get_type_by_url(response.url), sub_scp_type='')
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
            tags = [a.extract() for a in response.css('div.page-tags>span>a::text')]
            link = response.url[30:]
            if link == '/taboo':
                link = '/scp-4000'
            if link == '/numbered':
                link = '/scp-cn-1100'
            # /scp-es-026 会跳转 '/scp-179'
            detail_item = ScpDetailItem(link=link, detail=detail_dom.extract().replace('  ', '').replace('\n', ''),
                                        not_found=0, tags=','.join(tags))
        else:
            detail_item = ScpDetailItem(link=response.url[30:], detail="null", not_found=1, tags='')
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

