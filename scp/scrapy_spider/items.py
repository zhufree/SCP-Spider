# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScpBaseItem(scrapy.Item):
    """
    base info for each item
    """
    # base info
    index = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    scp_type = scrapy.Field()
    sub_scp_type = scrapy.Field()
    # get when scrapy detail


# class ScpTaleItem(ScpBaseItem):
#     author = scrapy.Field()
#     created_time = scrapy.Field()
    # month = scrapy.Field()
    # page_code = scrapy.Field()


# FIXME 竞赛胜出文章
# class ScpContestArticleItem(ScpBaseItem):
#     author = scrapy.Field()
    # contest_name = scrapy.Field()
    # contest_link = scrapy.Field()


# class ScpContestItem(ScpBaseItem):
#     creator = scrapy.Field()


# class ScpEventItem(ScpBaseItem):
    # event_type = scrapy.Field()


# collection
# class ScpSettingItem(ScpBaseItem):
#     desc = scrapy.Field()
#     snippet = scrapy.Field()
#     subtext = scrapy.Field()


# collection
# class ScpStorySeriesItem(ScpBaseItem):
#     author = scrapy.Field()
#     snippet = scrapy.Field()


class ScpTagItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()


class ScpDetailItem(scrapy.Item):
    link = scrapy.Field()
    detail = scrapy.Field()
    not_found = scrapy.Field()
    tags = scrapy.Field()
    download_type = scrapy.Field()
