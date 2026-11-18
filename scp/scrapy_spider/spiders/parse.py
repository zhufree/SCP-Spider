# -*- coding: utf-8 -*-
"""Turn a catalog HTML page into ScpBaseItem rows."""
import logging
import re

from lxml.html import HTMLParser
from lxml.html import fromstring as html_fromstring
from pyquery import PyQuery as pq

# Wikidot pages are XHTML 1.0. PyQuery's default parser reads that as XML and
# then fails the HTML fallback on the same document.
_HTML_PARSER = HTMLParser(recover=True, encoding="utf-8")

from ..items import ScpBaseItem
from ..links import (
    CN_SERIES_LINK,
    LOST_SERIES_LINK,
    SERIES_LINK,
    normalize_link,
)
from .constants import DATA_TYPE, REPORT_SUBTYPES

logger = logging.getLogger(__name__)

LETTER_LIST = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0-9",
]
CONTEST_HINT = re.compile(r"竞赛|contest", re.I)
SKIP_PATH_PREFIXES = ("/system:", "/forum", "/javascript")


def parse_html(pq_doc, scp_type, page_index=1):
    pq_doc = document_of(pq_doc)
    if scp_type <= DATA_TYPE["scp-series-cn"]:
        return parse_series_html(pq_doc, scp_type)
    if DATA_TYPE["scp-series-cn"] < scp_type <= DATA_TYPE["scp-ex-cn"]:
        return parse_joke_and_ex_html(pq_doc, scp_type)
    if DATA_TYPE["scp-ex-cn"] < scp_type <= DATA_TYPE["tales-cn-by-page-name"]:
        return parse_tale_html(pq_doc, scp_type, page_index)
    if DATA_TYPE["canon-hub"] <= scp_type <= DATA_TYPE["canon-hub-cn"]:
        return parse_setting_html(pq_doc, scp_type)
    if DATA_TYPE["series-archive"] <= scp_type <= DATA_TYPE["series-archive-cn"]:
        return parse_story_series_html(pq_doc, scp_type, page_index)
    if scp_type == DATA_TYPE["reports-interviews-and-logs"]:
        return parse_report_html(pq_doc, page_index)
    if scp_type == DATA_TYPE["goi"]:
        return parse_goi_html(pq_doc)
    if scp_type == DATA_TYPE["art"]:
        return parse_art_html(pq_doc, page_index)
    if scp_type == DATA_TYPE["contest-archive"]:
        return parse_contest_list_html(pq_doc)
    if scp_type == DATA_TYPE["contest-archive-cn"]:
        return parse_contest_cn_html(pq_doc)
    if DATA_TYPE["wander"] <= scp_type <= DATA_TYPE["wander-cn"]:
        return parse_wander_html(pq_doc, scp_type, page_index)
    if scp_type == DATA_TYPE["scp-international"]:
        return parse_international_page(pq_doc, page_index)
    return []


def _item(title, link, scp_type, index, sub_scp_type="", author="", created_time=""):
    link = normalize_link(link)
    if not link or _skipped_path(link):
        return None
    title = (title or "").strip() or link
    return ScpBaseItem(
        title=title,
        link=link,
        scp_type=scp_type,
        sub_scp_type=sub_scp_type or "",
        index=index,
        author=author or "",
        created_time=created_time or "",
    )


def _skipped_path(link):
    if link.startswith(SKIP_PATH_PREFIXES):
        return True
    # Catalog pages link to themselves and to tales-edition indexes.
    if link.endswith("-tales-edition"):
        return True
    return link in {
        "/contest-archive",
        "/contest-archive-cn",
        "/joke-scps",
        "/joke-scps-cn",
        "/scp-ex",
        "/scp-ex-cn",
    }


def _series_index(link, scp_type):
    if scp_type == DATA_TYPE["scp-series-cn"]:
        match = CN_SERIES_LINK.match(link)
        return int(match.group(1)) if match else None
    match = SERIES_LINK.match(link) or LOST_SERIES_LINK.match(link)
    return int(match.group(1)) if match else None


def parse_series_html(pq_doc, scp_type):
    """Keep numbered (and lost-series) entries. Header and warning links are skipped."""
    items = []
    seen = set()
    for anchor in pq_doc("#page-content ul li a").items():
        link = normalize_link(anchor.attr("href"))
        index = _series_index(link, scp_type)
        if index is None:
            if link:
                logger.debug("skip non-series link %s", link)
            continue
        if link in seen:
            continue
        seen.add(link)
        row = _item(anchor.closest("li").text(), link, scp_type, index)
        if row is not None:
            items.append(row)
    return items


def parse_joke_and_ex_html(pq_doc, scp_type):
    items = []
    seen = set()
    for index, li in enumerate(pq_doc("div.content-panel>ul>li").items()):
        link = li("a").attr("href")
        if not link or link in seen:
            continue
        seen.add(normalize_link(link))
        row = _item(li.text(), link, scp_type, index)
        if row is not None:
            items.append(row)
    return items


def parse_tale_html(pq_doc, scp_type, page_index=1):
    items = []
    sections = list(pq_doc("#page-content .section").items())
    for section_index, section in enumerate(sections):
        heading = section("h1, h2, h3, h4").text().strip()
        sub_type = heading if heading else (
            LETTER_LIST[section_index] if section_index < len(LETTER_LIST) else str(section_index)
        )
        letter_index = LETTER_LIST.index(sub_type) if sub_type in LETTER_LIST else section_index
        local = 0
        for row in section("div.list-pages-box tr").items():
            cells = list(row("td").items())
            if not cells:
                continue
            link = cells[0]("a").attr("href")
            if not link:
                continue
            author = cells[1].text().strip() if len(cells) > 1 else ""
            created = cells[2].text().strip() if len(cells) > 2 else ""
            index = letter_index * 1000000 + page_index * 10000 + local
            item = _item(
                cells[0].text(), link, scp_type, index, sub_type, author, created
            )
            local += 1
            if item is not None:
                items.append(item)
    return items


def parse_report_html(pq_doc, page_index=1):
    items = []
    tabs = _unique_tabs(pq_doc)
    local = 0
    for tab_index, tab in enumerate(tabs):
        sub_type = REPORT_SUBTYPES[tab_index] if tab_index < len(REPORT_SUBTYPES) else "tab-%s" % tab_index
        for li in tab(".list-pages-box > ul > li, .list-pages-box>ul>li").items():
            link = li("a").attr("href")
            item = _item(li("a").text() or li.text(), link, DATA_TYPE["reports-interviews-and-logs"],
                         page_index * 100000 + local, sub_type)
            local += 1
            if item is not None:
                items.append(item)
    return items


def parse_setting_html(pq_doc, scp_type):
    items = []
    seen = set()

    def add(title, link):
        row = _item(title, link, scp_type, len(items))
        if row is None or row["link"] in seen:
            return
        seen.add(row["link"])
        items.append(row)

    for block in pq_doc("div.centered").items():
        anchor = block("div.canon-title a")
        add(anchor.text(), anchor.attr("href"))
    for anchor in pq_doc("#page-content .canon-block h1 a").items():
        add(anchor.text(), anchor.attr("href"))
    if not items:
        for anchor in pq_doc("#page-content h1 a").items():
            add(anchor.text(), anchor.attr("href"))
    return items


def parse_goi_html(pq_doc):
    items = []
    seen = set()
    anchors = list(pq_doc("div.content-panel h2 a").items())
    anchors.extend(pq_doc("div.list-pages-box li a").items())
    for anchor in anchors:
        row = _item(anchor.text(), anchor.attr("href"), DATA_TYPE["goi"], len(items))
        if row is None or row["link"] in seen:
            continue
        seen.add(row["link"])
        items.append(row)
    return items


def parse_art_html(pq_doc, page_index=1):
    items = []
    seen = set()
    for row in pq_doc("div.content-panel tr").items():
        anchor = row("td > a")
        title = anchor.text()
        if not title:
            continue
        item = _item(title, anchor.attr("href"), DATA_TYPE["art"], page_index * 100000 + len(items))
        if item is None or item["link"] in seen:
            continue
        seen.add(item["link"])
        items.append(item)
    return items


def _contest_candidate(title, link):
    path = normalize_link(link)
    if not path:
        return False
    slug = path.rsplit("/", 1)[-1]
    return CONTEST_HINT.search("%s %s" % (title or "", slug)) is not None


def parse_contest_list_html(pq_doc):
    """Contest hubs across the year sections, not the winning works in the summary table."""
    items = []
    seen = set()
    for anchor in pq_doc("#page-content a").items():
        title = anchor.text()
        link = anchor.attr("href")
        if not _contest_candidate(title, link):
            continue
        row = _item(title, link, DATA_TYPE["contest-archive"], len(items))
        if row is None or row["link"] in seen:
            continue
        seen.add(row["link"])
        items.append(row)
    return items


def parse_contest_cn_html(pq_doc):
    items = []
    seen = set()
    for heading in pq_doc("#main-content h3, #page-content h3").items():
        anchors = list(heading("a").items())
        if not anchors:
            continue
        anchor = anchors[0]
        row = _item(anchor.text(), anchor.attr("href"), DATA_TYPE["contest-archive-cn"], len(items))
        if row is None or row["link"] in seen:
            continue
        seen.add(row["link"])
        items.append(row)
    return items


def parse_wander_html(pq_doc, scp_type, page_index=1):
    books = list(pq_doc("a.book").items())
    if books:
        return _parse_wander_books(pq_doc, scp_type, books)
    return _parse_wander_links(pq_doc, scp_type, page_index)


def _parse_wander_books(pq_doc, scp_type, books):
    items = []
    tabs = list(pq_doc("div.yui-content > div").items())
    if not tabs:
        for index, anchor in enumerate(books):
            row = _item(anchor("span.title").text() or anchor.text(), anchor.attr("href"), scp_type, index, "")
            if row is not None:
                items.append(row)
        return items
    index = 0
    for tab_index, tab in enumerate(tabs):
        sub_type = LETTER_LIST[tab_index] if tab_index < len(LETTER_LIST) else str(tab_index)
        for anchor in tab("a.book").items():
            row = _item(
                anchor("span.title").text() or anchor.text(),
                anchor.attr("href"),
                scp_type,
                index,
                sub_type,
            )
            index += 1
            if row is not None:
                items.append(row)
    return items


def _parse_wander_links(pq_doc, scp_type, page_index):
    items = []
    seen = set()
    for anchor in pq_doc("#page-content a").items():
        link = normalize_link(anchor.attr("href"))
        if not link or not link.startswith("/wanderers:"):
            continue
        if link in (
            "/wanderers:the-index",
            "/wanderers:the-index-cn",
            "/wanderers:the-library-cn",
            "/wanderers:start",
        ):
            continue
        row = _item(anchor.text(), link, scp_type, page_index * 100000 + len(items))
        if row is None or row["link"] in seen:
            continue
        seen.add(row["link"])
        items.append(row)
    return items


def parse_story_series_html(pq_doc, scp_type, page_index=1):
    items = []
    local = 0
    for row in pq_doc("div.list-pages-box tr").items():
        cells = list(row("td").items())
        if not cells:
            continue
        link = cells[0]("a").attr("href")
        if not link:
            continue
        author = cells[1].text().strip() if len(cells) > 1 else ""
        item = _item(
            cells[0].text(),
            link,
            scp_type,
            page_index * 100000 + local,
            "",
            author,
        )
        local += 1
        if item is not None:
            items.append(item)
    return items


def parse_international_page(pq_doc, page_index=1):
    items = []
    labels = _international_labels(pq_doc)
    tabs = _unique_tabs(pq_doc)
    index = page_index * 100000
    for tab_index, tab in enumerate(tabs):
        country = labels[tab_index] if tab_index < len(labels) else "tab-%s" % tab_index
        content_type = ""
        for node in tab.children().items():
            if node.is_("h1"):
                content_type = _international_kind(node.text())
            elif node.is_("ul") or node.is_(".list-pages-box"):
                for li in node("li").items():
                    row = _item(
                        li.text(),
                        li("a").attr("href"),
                        DATA_TYPE["scp-international"],
                        index,
                        country + "-" + content_type,
                    )
                    index += 1
                    if row is not None:
                        items.append(row)
    return items


def _international_kind(text):
    text = (text or "").strip()
    mapping = {
        "SCP系列": "series",
        "搞笑SCP系列": "joke",
        "被归档SCP系列": "arc",
        "故事": "tale",
        "其他": "other",
    }
    return mapping.get(text, text)


def _international_labels(pq_doc):
    navs = list(pq_doc("ul.yui-nav").items())
    if not navs:
        return []
    nav = max(navs, key=lambda node: len(list(node("li").items())))
    return [em.text().strip() for em in nav("li a em").items()]


def _unique_tabs(pq_doc):
    tabs = []
    seen = set()
    for tab in pq_doc('div[id^="wiki-tab-0-"]').items():
        tab_id = tab.attr("id")
        if not tab_id or tab_id in seen:
            continue
        seen.add(tab_id)
        tabs.append(tab)
    return tabs


def document_of(html):
    if isinstance(html, pq):
        return html
    if isinstance(html, bytes):
        html = html.decode("utf-8", "replace")
    html = (html or "").replace("\x00", "")
    root = html_fromstring(html.encode("utf-8"), parser=_HTML_PARSER)
    return pq(root)
