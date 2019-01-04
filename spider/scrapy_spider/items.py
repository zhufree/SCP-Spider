# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScpArticleItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    scp_type = scrapy.Field()
    detail = scrapy.Field()
    not_found = scrapy.Field()
    download_type = scrapy.Field()
    author = scrapy.Field()
    created_time = scrapy.Field()
    month = scrapy.Field()
    event_type = scrapy.Field()
    page_code = scrapy.Field()
    tags = scrapy.Field()


class ScpCollectionItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    scp_type = scrapy.Field()
    detail = scrapy.Field()
    desc = scrapy.Field()
    not_found = scrapy.Field()
    download_type = scrapy.Field()
    snippet = scrapy.Field()
    subtext = scrapy.Field()
    contest_name = scrapy.Field()
    contest_link = scrapy.Field()


class ScpTagItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()

