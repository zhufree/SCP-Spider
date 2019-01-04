# -*- coding: utf-8 -*-
# 解析html获取需要的链接或正文

from pyquery import PyQuery as pq
from ..constants import HEADERS, DATA_TYPE


def parse_html(pq_doc, scp_type):
    if scp_type == DATA_TYPE['scp-series']:
        return parse_series_html(pq_doc, scp_type)


# scp系列
def parse_series_html(pq_doc, scp_type):
    base_info_list = []
    end_index = scp_type == -3 if scp_type == DATA_TYPE['scp-series'] else -1
    for ul in list(pq_doc('div#page-content ul').items())[1:end_index]:
        for li in ul('li').items():
            link = li('a').attr('href')
            new_article = {
                'title': li.text(),
                'link': link,
                'scp_type': scp_type,
            }
            # base_info_list.append(link)
            print(link)
            base_info_list.append(new_article)

    return base_info_list
