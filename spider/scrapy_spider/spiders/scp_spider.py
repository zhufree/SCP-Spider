import scrapy
from pyquery import PyQuery as pq
from ...constants import DATA_TYPE, ENDPOINTS, HEADERS
from ..items import ScpArticleItem, ScpCollectionItem, ScpTagItem


class ScpListSpider(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "main_list_spider"  # 定义蜘蛛名
    allowed_domains = 'scp-wiki-cn.wikidot.com'

    start_urls = [
        # scp系列1-5
        # 'http://scp-wiki-cn.wikidot.com/scp-series',
        # 'http://scp-wiki-cn.wikidot.com/scp-series-2',
        # 'http://scp-wiki-cn.wikidot.com/scp-series-3',
        # 'http://scp-wiki-cn.wikidot.com/scp-series-4',
        # 'http://scp-wiki-cn.wikidot.com/scp-series-5',
        # scp cn 系列
        # 'http://scp-wiki-cn.wikidot.com/scp-series-cn',
        # 'http://scp-wiki-cn.wikidot.com/scp-series-cn-2',
        # tag
        # 'http://scp-wiki-cn.wikidot.com/system:page-tags/',
    ]

    def parse(self, response):
        pq_doc = pq(response.body)
        detail_request = scrapy.Request(response.urljoin(link), callback=self.parse_detail, headers=HEADERS)
        detail_request.meta['item'] = new_scp
        yield detail_request

    def parse_detail(self, response):
        item = response.meta['item']
        if response.status != 404:
            detail_dom = response.css('div#page-content')[0]
            item['detail'] = detail_dom.extract().replace('  ', '').replace('\n', '')
            item['not_found'] = 'false'
        else:
            item['detail'] = "<h3>抱歉，该页面尚无内容</h3>"
            item['not_found'] = 'true'
        # for category in total_scps_list:
        #     if category['link'] == link:
        #         category['not_found'] = "false"
        #         category['detail'] = detail_dom.html().replace('  ', '').replace('\n', '')
        yield item
        # a_in_detail = detail_dom.remove('.footer-wikiwalk-nav')('a')
        # if len(list(a_in_detail.items())) > 30:
        #     return
        # for a in a_in_detail.items():
        #     href = a.attr('href')
        #     if href.startswith('/') and href not in total_link_list:
        #         print('new link = ' + href)
        #         new_link.append(href)
        #         new_found_link_list.append(href)
        #         title = a.text()
        #         new_category = {
        #             'title': title,
        #             'link': href,
        #             'type': 'none'
        #         }
        #         new_found_category_list.append(new_category)


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
