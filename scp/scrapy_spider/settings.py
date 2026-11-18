# -*- coding: utf-8 -*-

BOT_NAME = "scrapy_spider"

SPIDER_MODULES = ["scrapy_spider.spiders"]
NEWSPIDER_MODULE = "scrapy_spider.spiders"

USER_AGENT = "SCP-Spider/1.0 (personal archive; low rate)"

# Wikidot's robots.txt allows normal article and /p/N URLs.
# It disallows stacked pagination (/p/1/p/2) and the voltron user agent.
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2
DOWNLOAD_DELAY = 0.3
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 3
LOG_LEVEL = "INFO"

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    "scrapy_spider.pipelines.ScpSpiderPipeline": 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 30
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.5

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
