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
    link = scrapy.Field()
    title = scrapy.Field()
    scp_type = scrapy.Field()
    # get when scrapy detail
    detail = scrapy.Field()
    not_found = scrapy.Field()
    # change by sql query and may change when needed
    download_type = scrapy.Field()
    tags = scrapy.Field()


class ScpTaleItem(ScpBaseItem):
    author = scrapy.Field()
    created_time = scrapy.Field()
    month = scrapy.Field()
    page_code = scrapy.Field()


class ScpContestItem(ScpBaseItem):
    author = scrapy.Field()
    month = scrapy.Field()
    page_code = scrapy.Field()
    contest_name = scrapy.Field()
    contest_link = scrapy.Field()


class ScpEventItem(ScpBaseItem):
    event_type = scrapy.Field()


class ScpSettingItem(ScpBaseItem):
    desc = scrapy.Field()
    snippet = scrapy.Field()
    subtext = scrapy.Field()


class ScpStorySeriesItem(ScpBaseItem):
    author = scrapy.Field()
    snippet = scrapy.Field()


class ScpTagItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()


class ScpDetailItem(scrapy.Item):
    link = scrapy.Field()
    detail = scrapy.Field()
    not_found = scrapy.Field()
