from pyquery import PyQuery as pq
from .constants import DATA_TYPE, HEADERS, SERIES_ENDPOINTS, SERIES_CN_ENDPOINTS, ENDPOINTS, REVERSE_ENDPOINTS, \
    SINGLE_PAGE_ENDPOINT, DB_NAME, URL_PARAMS
from ..items import *
from .parse import parse_html
import sqlite3


def get_type_by_url(url):
    if url in SERIES_ENDPOINTS:
        return DATA_TYPE['scp-series']
    elif url in SERIES_CN_ENDPOINTS:
        return DATA_TYPE['scp-series-cn']
    elif url in SINGLE_PAGE_ENDPOINT:
        return DATA_TYPE['single-page']
    elif url in ENDPOINTS.values():
        return DATA_TYPE[REVERSE_ENDPOINTS[url]]
    else:
        return -1


def get_empty_link_for_detail():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scps where detail is NULL;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list


def get_404_link_for_detail():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('select link from scps where not_found = 1;')
    link_list = [t[0] for t in cur]
    con.close()
    return link_list


class ScpListSpider(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "main_list_spider"  # 定义蜘蛛名
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    start_urls = \
        list(ENDPOINTS.values())

    # SERIES_ENDPOINTS + \
    # SERIES_CN_ENDPOINTS + \

    def parse(self, response):
        pq_doc = pq(response.body)
        base_info_list = parse_html(pq_doc, get_type_by_url(response.url))
        for info in base_info_list:
            new_scp = ScpBaseItem(info)
            yield new_scp


class ScpSinglePageSpider(scrapy.Spider):
    """
    抓取单页面
    """
    name = "single_page_spider"
    allowed_domains = 'scp-wiki-cn.wikidot.com'
    start_urls = SINGLE_PAGE_ENDPOINT

    def parse(self, response):
        pq_doc = pq(response.body)
        new_scp = ScpBaseItem(link=response.url[30:], title=pq_doc('div#page-title').text(),
                              scp_type=DATA_TYPE['single-page'])
        yield new_scp


class ScpDetailSpider(scrapy.Spider):
    name = 'detail_spider'
    allowed_domains = 'scp-wiki-cn.wikidot.com'
    start_urls = [('{_s_}://{_d_}' + link).format(**URL_PARAMS) for link in get_empty_link_for_detail()]
    handle_httpstatus_list = [404]  # 处理404页面，否则将会跳过

    def parse(self, response):
        if response.status != 404:
            detail_dom = response.css('div#page-content')[0]
            detail_item = ScpDetailItem(link=response.url[30:],
                                        detail=detail_dom.extract().replace('  ', '').replace('\n', ''), not_found=0)
        else:
            detail_item = ScpDetailItem(link=response.url[30:], detail="<h3>抱歉，该页面尚无内容</h3>", not_found=1)
        yield detail_item


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
