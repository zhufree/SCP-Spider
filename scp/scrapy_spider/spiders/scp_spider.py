# -*- coding: utf-8 -*-
import re
import sqlite3

import scrapy

from ..items import ScpBaseItem, ScpDetailItem
from ..links import child_links, extra_page_urls, normalize_link, page_number
from .constants import (
    CN_SERIES_PROBE_MAX,
    DATA_TYPE,
    DETAIL_DB_NAME,
    HEADERS,
    INFO_PAGE,
    LIBRARY_PAGE,
    LIST_SEED_URLS,
    PAGINATED_SINGLE_PAGES,
    SERIES_PROBE_MAX,
    URL_BASE,
)
from .parse import document_of, parse_html

_TYPE_RULES = (
    (re.compile(r"^/scp-series-cn(?:-\d+)?$"), "scp-series-cn"),
    (re.compile(r"^/scp-series(?:-\d+)?$"), "scp-series"),
    (re.compile(r"^/lost-scp-series$"), "scp-series"),
    (re.compile(r"^/joke-scps-cn$"), "joke-scps-cn"),
    (re.compile(r"^/joke-scps$"), "joke-scps"),
    (re.compile(r"^/scp-ex-cn$"), "scp-ex-cn"),
    (re.compile(r"^/scp-ex$"), "scp-ex"),
    (re.compile(r"^/tales-cn-by-page-name$"), "tales-cn-by-page-name"),
    (re.compile(r"^/tales-by-page-name$"), "tales-by-page-name"),
    (re.compile(r"^/canon-hub-cn$"), "canon-hub-cn"),
    (re.compile(r"^/canon-hub$"), "canon-hub"),
    (re.compile(r"^/series-archive-cn$"), "series-archive-cn"),
    (re.compile(r"^/series-archive$"), "series-archive"),
    (re.compile(r"^/incident-reports-eye-witness-interviews-and-personal-logs$"), "reports-interviews-and-logs"),
    (re.compile(r"^/scp-artwork-hub$"), "art"),
    (re.compile(r"^/goi-formats$"), "goi"),
    (re.compile(r"^/contest-archive-cn$"), "contest-archive-cn"),
    (re.compile(r"^/contest-archive$"), "contest-archive"),
    (re.compile(r"^/wanderers:the-index-cn$"), "wander-cn"),
    (re.compile(r"^/wanderers:the-library-cn$"), "wander-cn"),
    (re.compile(r"^/wanderers:the-index$"), "wander"),
    (re.compile(r"^/scp-international$"), "scp-international"),
    (re.compile(r"^/log-of-anomalous-items-cn$"), "log-of-anomalous-page-cn"),
    (re.compile(r"^/short-stories$"), "short-story"),
)

_LIBRARY_PATHS = {normalize_link(url) for url in LIBRARY_PAGE}
_INFO_PATHS = {normalize_link(url) for url in INFO_PAGE}
_PAGINATED_SINGLE_PATHS = {normalize_link(url) for url in PAGINATED_SINGLE_PAGES}


def catalog_path(url):
    path = normalize_link(url) or ""
    if not path and "://" not in url:
        path = url.split("?")[0]
    path = re.sub(r"/p/\d+$", "", path)
    return path


def get_type_by_url(url):
    path = catalog_path(url)
    if path in _LIBRARY_PATHS:
        return DATA_TYPE["library-single-page"]
    if path in _INFO_PATHS:
        return DATA_TYPE["info-single-page"]
    for pattern, name in _TYPE_RULES:
        if pattern.match(path):
            return DATA_TYPE[name]
    return -1


def series_url(kind, number):
    if kind == "cn":
        if number == 1:
            return URL_BASE + "/scp-series-cn"
        return "%s/scp-series-cn-%s" % (URL_BASE, number)
    if number == 1:
        return URL_BASE + "/scp-series"
    return "%s/scp-series-%s" % (URL_BASE, number)


def _empty_detail_links():
    con = sqlite3.connect(DETAIL_DB_NAME)
    try:
        rows = con.execute("SELECT link FROM scp_detail WHERE detail IS NULL")
        return [row[0] for row in rows if row[0] and "http" not in row[0]]
    finally:
        con.close()


def _saved_child_links():
    con = sqlite3.connect(DETAIL_DB_NAME)
    try:
        rows = con.execute(
            "SELECT link, detail FROM scp_detail WHERE detail IS NOT NULL AND not_found IS NOT 1"
        )
        found = []
        seen = set()
        for link, detail in rows:
            for child in child_links(link, detail or ""):
                if child not in seen:
                    seen.add(child)
                    found.append(child)
        return found
    finally:
        con.close()


class ScpTestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["scp-wiki-cn.wikidot.com"]
    start_urls = [URL_BASE + "/scp-series"]

    def parse(self, response):
        yield from emit_catalog(response)


class ScpListSpider(scrapy.Spider):
    """Catalog pages. Series numbers and /p/N pages are discovered, not hard-coded."""

    name = "main"
    allowed_domains = ["scp-wiki-cn.wikidot.com"]
    handle_httpstatus_list = [404]

    def start_requests(self):
        for url in LIST_SEED_URLS:
            yield scrapy.Request(url, callback=self.parse, headers=HEADERS)
        yield scrapy.Request(
            series_url("en", 1),
            callback=self.parse_series_chain,
            headers=HEADERS,
            meta={"kind": "en", "n": 1},
        )
        yield scrapy.Request(
            series_url("cn", 1),
            callback=self.parse_series_chain,
            headers=HEADERS,
            meta={"kind": "cn", "n": 1},
        )

    def parse_series_chain(self, response):
        kind = response.meta["kind"]
        number = response.meta["n"]
        if response.status != 404:
            yield from self.parse(response)
            limit = CN_SERIES_PROBE_MAX if kind == "cn" else SERIES_PROBE_MAX
            if number < limit:
                yield scrapy.Request(
                    series_url(kind, number + 1),
                    callback=self.parse_series_chain,
                    headers=HEADERS,
                    meta={"kind": kind, "n": number + 1},
                )
        else:
            self.logger.info("series chain %s stops at %s", kind, number)

    def parse(self, response):
        if response.status == 404:
            return
        yield from emit_catalog(response)
        for url in extra_page_urls(response.url, response.text):
            yield scrapy.Request(url, callback=self.parse, headers=HEADERS)


class ScpSinglePageSpider(scrapy.Spider):
    """Pages stored as one row each. Anomalous-item and short-story lists follow their pager."""

    name = "single"
    allowed_domains = ["scp-wiki-cn.wikidot.com"]
    start_urls = LIBRARY_PAGE + INFO_PAGE + PAGINATED_SINGLE_PAGES

    def parse(self, response):
        document = document_of(response.text)
        title = document("#page-title").text().strip()
        number = page_number(response.url)
        if number > 1:
            title = "%s %s" % (title, number)
        link = normalize_link(response.url)
        yield ScpBaseItem(
            index=number,
            link=link,
            title=title or link,
            scp_type=get_type_by_url(response.url),
            sub_scp_type="",
            author="",
            created_time="",
        )
        if catalog_path(response.url) in _PAGINATED_SINGLE_PATHS:
            for url in extra_page_urls(response.url, response.text):
                yield scrapy.Request(url, callback=self.parse, headers=HEADERS)


class ScpDetailSpider(scrapy.Spider):
    """Fill empty detail rows. Whitespace inside the article is kept."""

    name = "detail"
    allowed_domains = ["scp-wiki-cn.wikidot.com"]
    handle_httpstatus_list = [404]

    def start_requests(self):
        for link in _empty_detail_links():
            yield scrapy.Request(
                URL_BASE + link,
                callback=self.parse,
                headers=HEADERS,
                meta={"link": link},
            )

    def parse(self, response):
        link = response.meta.get("link") or normalize_link(response.url)
        if response.status == 404:
            yield ScpDetailItem(link=link, detail="null", not_found=1, tags="")
            return
        content = response.css("div#page-content")
        if not content:
            self.logger.warning("no page-content on %s", link)
            return
        html = content.get()
        tags = response.css("div.page-tags a::text").getall()
        yield ScpDetailItem(
            link=link,
            detail=html,
            not_found=0,
            tags=",".join(tag.strip() for tag in tags if tag.strip()),
        )
        for child in child_links(link, html):
            yield scrapy.Request(
                URL_BASE + child,
                callback=self.parse_child,
                headers=HEADERS,
                meta={"link": child, "parent": link},
            )

    def parse_child(self, response):
        link = response.meta["link"]
        parent = response.meta.get("parent") or link
        if response.status == 404:
            yield ScpDetailItem(link=link, detail="null", not_found=1, tags="")
            return
        content = response.css("div#page-content")
        if not content:
            return
        html = content.get()
        title = ""
        heading = response.css("div#page-title::text").get()
        if heading:
            title = heading.strip()
        if "/offset/" in link:
            title = "%s-offset-%s" % (title or parent, link.rsplit("/", 1)[-1])
        yield ScpBaseItem(
            index=0,
            link=link,
            title=title or link,
            scp_type=DATA_TYPE["offset"],
            sub_scp_type="",
            author="",
            created_time="",
        )
        yield ScpDetailItem(link=link, detail=html, not_found=0, tags="")
        for child in child_links(parent, html):
            if child == link:
                continue
            yield scrapy.Request(
                URL_BASE + child,
                callback=self.parse_child,
                headers=HEADERS,
                meta={"link": child, "parent": parent},
            )


class ScpOffsetSpider(scrapy.Spider):
    """Backfill offset and fragment pages linked from details already saved."""

    name = "offset"
    allowed_domains = ["scp-wiki-cn.wikidot.com"]
    handle_httpstatus_list = [404]

    def start_requests(self):
        for link in _saved_child_links():
            yield scrapy.Request(
                URL_BASE + link,
                callback=self.parse,
                headers=HEADERS,
                meta={"link": link, "parent": link.split("/offset/")[0]},
            )

    def parse(self, response):
        yield from ScpDetailSpider.parse_child(self, response)


def emit_catalog(response):
    scp_type = get_type_by_url(response.url)
    if scp_type < 0:
        return
    document = document_of(response.text)
    for item in parse_html(document, scp_type, page_number(response.url)):
        yield item
