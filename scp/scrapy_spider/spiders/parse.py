# -*- coding: utf-8 -*-
# 解析html获取需要的链接或正文

from .constants import DATA_TYPE
from ..items import *


def get_tale_year_by_time(time):
    year = time.split(' ')[2]
    month = time.split(' ')[1]
    return year + month


def parse_html(pq_doc, scp_type):
    if scp_type <= DATA_TYPE['scp-series-cn']:
        return parse_series_html(pq_doc, scp_type)
    elif DATA_TYPE['scp-series-cn'] < scp_type <= DATA_TYPE['scp-ex-cn']:
        return parse_joke_and_ex_html(pq_doc, scp_type)
    elif DATA_TYPE['scp-ex-cn'] < scp_type <= DATA_TYPE['tales-cn-by-page-name']:
        return parse_tale_html(pq_doc, scp_type)
    elif DATA_TYPE['canon-hub'] <= scp_type <= DATA_TYPE['canon-hub-cn']:
        return parse_setting_html(pq_doc, scp_type)
    elif DATA_TYPE['series-archive'] <= scp_type <= DATA_TYPE['series-archive-cn']:
        return parse_story_series_html(pq_doc, scp_type)
    elif scp_type == DATA_TYPE['reports-interviews-and-logs']:
        return parse_report_html(pq_doc)
    elif scp_type == DATA_TYPE['goi']:
        return parse_goi_html(pq_doc)
    elif scp_type == DATA_TYPE['art']:
        return parse_art_html(pq_doc)
    elif scp_type == DATA_TYPE['contest-archive']:
        return parse_contest_list_html(pq_doc)
    elif scp_type == DATA_TYPE['contest-archive-cn']:
        return parse_contest_cn_html(pq_doc)
    elif DATA_TYPE['wander'] <= scp_type <= DATA_TYPE['wander-cn']:
        return parse_wander_html(pq_doc, scp_type)
    elif scp_type == DATA_TYPE['scp-international']:
        return parse_international_page(pq_doc)


# scp系列
def parse_series_html(pq_doc, scp_type):
    base_info_list = []
    end_index = -3 if scp_type == DATA_TYPE['scp-series'] else -2
    start_index = 2 if scp_type == DATA_TYPE['scp-series'] else 1
    for ul in list(pq_doc('div#page-content ul').items())[start_index:end_index]:
        for li in ul('li').items():
            link = li('a').attr('href')
            if link == '/1231-warning':
                link = '/scp-1231'
            if link == None:
                link = '/'
            if 'scp-wiki-cn.wikidot.com' in link:
                link = link[30:]
            link_part = link.split('-')
            index = -1
            if len(link_part) > 1:
                index = int(link_part[1 if scp_type == DATA_TYPE['scp-series'] else 2])
            new_article = {
                'title': li.text(),
                'link': link,
                'scp_type': scp_type,
                'sub_scp_type': '',
                'index': index
            }
            base_info_list.append(ScpBaseItem(new_article))
    return base_info_list


LETTER_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']


def parse_tale_html(pq_doc, scp_type):
    tale_list = []
    index = 0
    for i in range(0, 27):
        for section_tr in list(list(pq_doc('div#page-content .section').items())[i]('div.list-pages-box tr').items()):
            tds = list(section_tr('td').items())
            new_tale = {
                'title': tds[0].text(),
                'link': tds[0]('a').attr('href'),
                # 'author': tds[1].text(),
                # 'created_time': tds[2].text(),
                'scp_type': scp_type,
                'sub_scp_type': LETTER_LIST[i],
                'index': index
            }
            tale_list.append(ScpBaseItem(new_tale))
            index += 1
    return tale_list


def parse_joke_and_ex_html(pq_doc, scp_type):
    base_info_list = []
    index = 0
    parse_path = 'div.content-panel>ul>li'
    for li in list(pq_doc(parse_path).items()):
        link = li('a').attr('href')
        if 'http://scp-wiki-cn.wikidot.com' in link:
            link = link[30:]
        new_article = {
            'title': li.text(),
            'link': link,
            'scp_type': scp_type,
            'sub_scp_type': '',
            'index': index
        }
        base_info_list.append(ScpBaseItem(new_article))
        index += 1
    return base_info_list


report_index = 0


def parse_report_html(pq_doc):
    global report_index
    item_list = []
    for i in range(0, 5):
        for li in pq_doc('#wiki-tab-0-' + str(i) + ' .list-pages-box>ul>li').items():
            new_article = {
                'link': li('a').attr('href'),
                'title': li('a').text(),
                'scp_type': DATA_TYPE['reports-interviews-and-logs'],
                'index': report_index
            }
            if i == 0:
                new_article['sub_scp_type'] = 'lab_record'
            elif i == 1:
                new_article['sub_scp_type'] = 'discovery_report'
            elif i == 2:
                new_article['sub_scp_type'] = 'event_report'
            elif i == 3:
                new_article['sub_scp_type'] = 'interview'
            elif i == 4:
                new_article['sub_scp_type'] = 'addon'
            item_list.append(ScpBaseItem(new_article))
            report_index += 1
    return item_list


def parse_setting_html(pq_doc, scp_type):
    setting_list = []
    index = 0
    for div in list(pq_doc('div.centered').items()):
        new_article = {
            'title': div('div.canon-title a').text(),
            'link': div('div.canon-title a').attr('href'),
            # 'desc': div('div.canon-description').text(),
            # 'snippet': div('div.canon-snippet').text(),
            # 'subtext': div('div.canon-snippet-subtext').text(),
            'scp_type': scp_type,
            'sub_scp_type': '',
            'index': index
        }
        setting_list.append(ScpBaseItem(new_article))
        index += 1
    return setting_list


def parse_goi_html(pq_doc):
    art_list = []
    index = 0
    h2_parse_path = 'div.content-panel h2'
    item_parse_path = 'div.list-pages-box li'
    for h2 in list(pq_doc(h2_parse_path).items()):
        link = h2('a').attr('href')
        title = h2('a').text()
        if link != '' and link is not None:
            new_article = {
                'title': title,
                'link': link,
                'scp_type': DATA_TYPE['goi'],
                'sub_scp_type': '',
                'index': index
            }
            art_list.append(ScpBaseItem(new_article))
            index += 1
    for item in list(pq_doc(item_parse_path).items()):
        link = item('a').attr('href')
        title = item('a').text()
        if link != '' and link is not None:
            new_article = {
                'title': title,
                'link': link,
                'scp_type': DATA_TYPE['goi'],
                'sub_scp_type': '',
                'index': index
            }
            art_list.append(ScpBaseItem(new_article))
            index += 1
    return art_list


art_index = 0


def parse_art_html(pq_doc):
    global art_index
    art_list = []
    parse_path = 'div.content-panel tr'
    for tr in list(pq_doc(parse_path).items()):
        title = tr('td>a').text()
        if title != '':
            new_article = {
                'title': title,
                'link': tr('td>a').attr('href'),
                'scp_type': DATA_TYPE['art'],
                'sub_scp_type': '',
                'index': art_index
            }
            art_list.append(ScpBaseItem(new_article))
            art_index += 1
    return art_list


def parse_contest_list_html(pq_doc):
    contest_list = []
    index = 0
    for section_tr in list(pq_doc('div#page-content .content-type-description>table tr').items())[2:]:
        tds = list(section_tr('td').items())
        current_contest_name = tds[0].text()
        current_contest_link = tds[0]('a').attr('href')
        if current_contest_name is not None and len(current_contest_name) > 2:
            if 'http://scp-wiki-cn.wikidot.com' in current_contest_link:
                current_contest_link = current_contest_link[30:]
            last_contest_name = current_contest_name
            last_contest_link = current_contest_link
            new_contest = {
                'title': last_contest_name,
                'link': last_contest_link,
                'scp_type': DATA_TYPE['contest-archive'],
                'sub_scp_type': '',
                # 'creator': tds[1].text(),
                'index': index
            }
            index += 1
            contest_list.append(ScpBaseItem(new_contest))
    return contest_list


def parse_contest_cn_html(pq_doc):
    contest_list = []
    h3_list = list(pq_doc('div#main-content h3').items())
    index = 0
    for i in range(len(h3_list)):
        h3 = h3_list[i]
        contest_a = list(h3('a').items())[0]
        current_p = list(h3.siblings('p').items())[i]
        current_holder = list(current_p('span:first').items())[0]
        new_contest = {
            'title': contest_a.text(),
            'link': contest_a.attr('href'),
            'scp_type': DATA_TYPE['contest-archive-cn'],
            'sub_scp_type': '',
            # 'creator': list(current_holder('a').items())[1].text(),
            'index': index
        }
        index += 1
        contest_list.append(ScpBaseItem(new_contest))
    return contest_list


def parse_wander_html(pq_doc, scp_type):
    wander_list = []
    index = 0
    tabs = list(pq_doc('div.yui-content>div').items())
    print(len(tabs))
    for i in range(0, 27):
        for a in list(tabs[i]('a.book').items()):
            new_article = {
                'title': a('span.title').text(),
                'link': a.attr('href'),
                'scp_type': scp_type,
                'sub_scp_type': LETTER_LIST[i],
                'index': index
            }
            wander_list.append(ScpBaseItem(new_article))
            index += 1
    return wander_list


story_index = 0


def parse_story_series_html(pq_doc, scp_type):
    story_series_list = []
    global story_index
    for tr in list(pq_doc('div.list-pages-box tr').items())[1:]:
        tds = list(tr('td').items())
        new_article = {
            'title': tds[0].text(),
            'link': tds[0]('a').attr('href'),
            # 'author': tds[1].text(),
            # 'snippet': tds[2].text(),
            'scp_type': scp_type,
            'sub_scp_type': '',
            'index': story_index
        }
        story_index += 1
        story_series_list.append(ScpBaseItem(new_article))
    return story_series_list


# articles in contest page
def parse_collection_item_html(pq_doc, scp_type):
    content_article_list = []
    index = 0
    for elm_a in list(pq_doc('div#page-content a').items()):
        link = elm_a.attr('href')
        if link is not None and 'forum' not in link \
                and 'user:info' not in link \
                and 'javascript' not in link \
                and not link.startswith('#') \
                and not (link.startswith('http') and 'scp-wiki-cn.wikidot.com' not in link):
            if 'http://scp-wiki-cn.wikidot.com' in link:
                link = link[30:]
            new_article = {
                'title': elm_a.text(),
                'link': link,
                'scp_type': scp_type,
                'index': index
            }
            index += 1
            content_article_list.append(ScpBaseItem(new_article))
    return content_article_list


def parse_international_page(pq_doc):
    """ 国际版 """
    international_list = []
    index = 0
    for i in range(0, 13):
        country_code = list(pq_doc('ul.yui-nav li a em').items())[i].text()
        # 列出 div#wiki-tab-0-%s 下的所有子元素
        # 遍历 h1标记为content_type
        # h1后面接的ul直到下一个h1
        # 或h1跟着div.list-pages-box再套着ul
        tab_item_list = list(pq_doc('div#wiki-tab-0-%s>*' % (str(i))).items())
        content_type = ''
        for j in range(0, len(tab_item_list)):
            current_item = tab_item_list[j]
            if current_item.is_('h1'):
                current_h1 = current_item
                if current_h1.text() == 'SCP系列':
                    content_type = 'series'
                elif current_h1.text() == '搞笑SCP系列':
                    content_type = 'joke'
                elif current_h1.text() == '被归档SCP系列':
                    content_type = 'arc'
                elif current_h1.text() == '故事':
                    content_type = 'tale'
                elif current_h1.text() == '其他':
                    content_type = 'other'
            elif current_item.is_('ul'):
                current_ul = current_item
                for li in list((current_ul('li')).items()):
                    new_article = {
                        'title': li.text(),
                        'link': li('a').attr('href'),
                        'scp_type': DATA_TYPE['scp-international'],
                        'sub_scp_type': country_code + '-' + content_type,
                        'index': index
                    }
                    international_list.append(ScpBaseItem(new_article))
                    index += 1
            elif current_item.is_('.list-pages-box'):
                for li in list(current_item('ul li').items()):
                    new_article = {
                        'title': li.text(),
                        'link': li('a').attr('href'),
                        'scp_type': DATA_TYPE['scp-international'],
                        'sub_scp_type': country_code + '-' + content_type,
                        'index': index
                    }
                    international_list.append(ScpBaseItem(new_article))
                    index += 1
    return international_list
