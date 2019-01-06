# -*- coding: utf-8 -*-
# 解析html获取需要的链接或正文

from .constants import DATA_TYPE, TALE_LETTER_LIST


def get_tale_year_by_time(time):
    year = time.split(' ')[2]
    month = time.split(' ')[1]
    return year+month


def parse_html(pq_doc, scp_type):
    if scp_type <= DATA_TYPE['scp-series-cn']:
        return parse_series_html(pq_doc, scp_type)
    elif DATA_TYPE['scp-series-cn'] < scp_type <= DATA_TYPE['tales-cn-by-page-name']:
        return parse_tale_html(pq_doc, scp_type)
    elif DATA_TYPE['tales-cn-by-page-name'] < scp_type <= DATA_TYPE['scp-removed']:
        return parse_archives_html(pq_doc, scp_type)


# scp系列
def parse_series_html(pq_doc, scp_type):
    base_info_list = []
    end_index = -3 if scp_type == DATA_TYPE['scp-series'] else -1
    for ul in list(pq_doc('div#page-content ul').items())[1:end_index]:
        for li in ul('li').items():
            link = li('a').attr('href')
            new_article = {
                'title': li.text(),
                'link': link,
                'scp_type': scp_type,
            }
            print(link)
            base_info_list.append(new_article)

    return base_info_list


def parse_tale_html(pq_doc, scp_type):
    tale_list = []
    for i in range(0, 27):
        for section_tr in list(list(pq_doc('div#page-content .section').items())[i]('div.list-pages-box tr').items()):
            tds = list(section_tr('td').items())
            new_tale = {
                'title': tds[0].text(),
                'link': tds[0]('a').attr('href'),
                'author': tds[1].text(),
                'created_time': tds[2].text(),
                'month': get_tale_year_by_time(tds[2].text()),
                'page_code': TALE_LETTER_LIST[i],
                'scp_type': scp_type
            }
            tale_list.append(new_tale)
    return tale_list


def parse_archives_html(pq_doc, scp_type):
    base_info_list = []
    parse_path = 'div#page-content div.content-panel ul li' if scp_type == DATA_TYPE[
        'archived-scps'] else 'div.content-panel>ul>li'
    for li in list(pq_doc(parse_path).items()):
        link = li('a').attr('href')
        new_article = {
            'title': li.text(),
            'link': link,
            'scp_type': scp_type
        }
        print(link)
        base_info_list.append(new_article)
    return base_info_list


# 这版本暂时不用
def parse_setting_html(pq_doc, scp_type):
    setting_list = []
    for div in list(pq_doc('div.centered').items()):
        new_article = {
            'title': div('div.canon-title a').text(),
            'link': div('div.canon-title a').attr('href'),
            'desc': div('div.canon-description').text(),
            'snippet': div('div.canon-snippet').text(),
            'subtext': div('div.canon-snippet-subtext').text(),
            'scp_type': scp_type
        }
        # link_list.append(new_article['link'])
        print(new_article['link'])
        setting_list.append(new_article)
    return setting_list


def parse_content_html(pq_doc):
    contest_list = []
    last_contest_name = ""
    last_contest_link = ""
    for section_tr in list(pq_doc('div#page-content .content-type-description>table tr').items())[2:]:
        new_article = {}
        tds = list(section_tr('td').items())
        current_contest_name = tds[0].text()
        current_contest_link = tds[0]('a').attr('href')
        if current_contest_name is not None and len(current_contest_name) > 2:
            last_contest_name = current_contest_name
            last_contest_link = current_contest_link
        else:
            current_contest_name = last_contest_name
            current_contest_link = last_contest_link

        if len(list(tds[2]('br').items())) != 0:
            new_plus_article = {}
            double_a = list(tds[2]('a').items())
            double_author = str(tds[3].html()).split('<br />')
            new_article['title'] = double_a[0].text()
            new_article['link'] = double_a[0].attr('href')
            new_article['author'] = double_author[0]
            new_plus_article['title'] = double_a[1].text()
            new_plus_article['link'] = double_a[1].attr('href')
            new_plus_article['author'] = double_author[1]
            new_article['contest_name'] = current_contest_name
            new_article['contest_link'] = current_contest_link
            new_plus_article['contest_name'] = current_contest_name
            new_plus_article['contest_link'] = tds[0]('a').attr('href')
            new_article['scp_type'] = DATA_TYPE['contest-archive']
            new_plus_article['scp_type'] = DATA_TYPE['contest-archive']

            if new_article['link'] is not None:
                contest_list.append(new_article)
            if new_plus_article['link'] is not None:
                contest_list.append(new_plus_article)
        else:
            new_article['title'] = tds[2].text()
            new_article['link'] = tds[2]('a').attr('href')
            new_article['author'] = tds[3].text()
            new_article['contest_name'] = current_contest_name
            new_article['contest_link'] = current_contest_link
            new_article['scp_type'] = DATA_TYPE['contest-archive']

            if new_article['link'] is not None:
                print(new_article['link'])
                contest_list.append(new_article)
    return contest_list


def parse_contest_cn_html(pq_doc):
    contest_list = []
    h3_list = list(pq_doc('div#main-content h3').items())
    for i in range(len(h3_list)):
        h3 = h3_list[i]
        current_p = list(h3.siblings('p').items())[i]
        current_holder = list(current_p('span:first').items())[0]
        for a in current_holder.siblings('a').items():
            new_article = {
                'title': a.text(),
                'link': a.attr('href'),
                'author': a.next('span.printuser>a:last').text(),
                'contest_name': h3('span').text(),
                'contest_link': h3('span>a').attr('href'),
                'scp_type': DATA_TYPE['contest-archive-cn']
            }
            
            print(new_article['link'])
            contest_list.append(new_article)
    return contest_list


def parse_story_series_html(pq_doc, scp_type):
    story_series_list = []
    for tr in list(pq_doc('div.list-pages-box tr').items())[1:]:
        tds = list(tr('td').items())
        new_article = {
            'title': tds[0].text(),
            'link': tds[0]('a').attr('href'),
            'author': tds[1].text(),
            'snippet': tds[2].text(),
            'scp_type': scp_type
        }
        story_series_list.append(new_article)
    return story_series_list
