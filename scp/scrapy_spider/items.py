# -*- coding: utf-8 -*-
import scrapy


class ScpBaseItem(scrapy.Item):
    index = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    scp_type = scrapy.Field()
    sub_scp_type = scrapy.Field()
    author = scrapy.Field()
    created_time = scrapy.Field()


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
