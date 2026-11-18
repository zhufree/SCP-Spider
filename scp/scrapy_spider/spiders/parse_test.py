# -*- coding: utf-8 -*-
import os
import sqlite3
import tempfile
import unittest

from scrapy_spider.links import child_links, extra_page_urls, normalize_link
from scrapy_spider.pipelines import upsert_category, upsert_detail
from scrapy_spider.spiders.constants import DATA_TYPE
from scrapy_spider.spiders.parse import parse_html
from scrapy_spider.spiders.scp_spider import get_type_by_url, series_url


SERIES_HTML = """
<div id="page-content">
  <ul><li><a href="/joke-scps">搞笑</a></li></ul>
  <ul><li><a href="/scp-removed">已删除</a></li></ul>
  <ul>
    <li><a href="/scp-1000">SCP-1000 - 甲</a></li>
    <li><a href="/902-warning">警告</a></li>
  </ul>
  <ul><li><a href="/scp-1800">SCP-1800 - 乙</a></li></ul>
  <ul><li><a href="/scp-1900">SCP-1900 - 丙</a></li></ul>
</div>
"""

LOST_HTML = """
<div id="page-content">
  <ul><li><a href="/scp-ex">已解明</a></li></ul>
  <ul><li><a href="/scp-l001">SCP-L001 - 失落</a></li></ul>
</div>
"""

CN_HTML = """
<div id="page-content">
  <ul><li><a href="/task-forces">机动特遣队</a></li></ul>
  <ul><li><a href="/scp-cn-4000">SCP-CN-4000 - 甲</a></li></ul>
  <ul><li><a href="/scp-cn-4900">SCP-CN-4900 - 乙</a></li></ul>
  <ul><li><a href="/joke-scps-cn">搞笑</a></li></ul>
  <ul><li><a href="/scp-series-cn-1-tales-edition">故事版</a></li></ul>
</div>
"""

TALE_HTML = """
<div id="page-content">
  <div class="section">
    <h3>A</h3>
    <div class="list-pages-box">
      <table>
        <tr><td>标题</td><td>作者</td><td>时间</td></tr>
        <tr>
          <td><a href="/a-baptism-of-fire">火之洗礼</a></td>
          <td>ahshow</td>
          <td>21 Jun 2026 15:00</td>
        </tr>
      </table>
    </div>
  </div>
</div>
"""

CANON_HTML = """
<div id="page-content">
  <div class="canon-block"><h1><a href="/aces-and-eights">死者手牌</a></h1></div>
</div>
"""

CANON_CN_HTML = """
<div id="page-content">
  <div class="centered"><div class="canon-title"><a href="/some-canon">某个设定</a></div></div>
</div>
"""

CONTEST_HTML = """
<div id="page-content">
  <h1>2019 - 2020</h1>
  <p><a href="/goi-contest-2014">相关组织竞赛！</a></p>
  <p><a href="/wanderers:forgotten">不可记忆之物</a></p>
  <p><a href="https://scp-wiki-cn.wikidot.com/halloween-contest">2012年万圣节竞赛</a></p>
  <p><a href="/contest-archive">征文竞赛</a></p>
</div>
"""

INTL_HTML = """
<div id="page-content">
  <ul class="yui-nav">
    <li><a href="#"><em>俄国分部</em></a></li>
    <li><a href="#"><em>印尼分部</em></a></li>
  </ul>
  <div id="wiki-tab-0-0">
    <h1>SCP系列</h1>
    <ul><li><a href="/scp-ru-001">SCP-RU-001</a></li></ul>
  </div>
  <div id="wiki-tab-0-1">
    <h1>故事</h1>
    <div class="list-pages-box"><ul><li><a href="/id-tale">一篇故事</a></li></ul></div>
  </div>
</div>
"""

WANDER_LIBRARY_HTML = """
<div id="page-content">
  <a href="/wanderers:the-library-cn">索引</a>
  <a href="/wanderers:potions-introduction">药水介绍</a>
</div>
"""


class ParseTests(unittest.TestCase):
    def test_series_keeps_last_blocks_and_skips_warnings(self):
        items = parse_html(SERIES_HTML, DATA_TYPE["scp-series"])
        links = [item["link"] for item in items]
        self.assertEqual(links, ["/scp-1000", "/scp-1800", "/scp-1900"])
        self.assertEqual(items[0]["index"], 1000)

    def test_lost_and_cn_series(self):
        lost = parse_html(LOST_HTML, DATA_TYPE["scp-series"])
        self.assertEqual([item["link"] for item in lost], ["/scp-l001"])
        cn = parse_html(CN_HTML, DATA_TYPE["scp-series-cn"])
        self.assertEqual([item["link"] for item in cn], ["/scp-cn-4000", "/scp-cn-4900"])

    def test_tale_keeps_author_and_time(self):
        items = parse_html(TALE_HTML, DATA_TYPE["tales-by-page-name"], page_index=2)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["author"], "ahshow")
        self.assertEqual(items[0]["created_time"], "21 Jun 2026 15:00")
        self.assertEqual(items[0]["sub_scp_type"], "A")

    def test_canon_blocks_and_legacy_cards(self):
        en = parse_html(CANON_HTML, DATA_TYPE["canon-hub"])
        self.assertEqual(en[0]["link"], "/aces-and-eights")
        cn = parse_html(CANON_CN_HTML, DATA_TYPE["canon-hub-cn"])
        self.assertEqual(cn[0]["link"], "/some-canon")

    def test_contest_skips_winning_works(self):
        items = parse_html(CONTEST_HTML, DATA_TYPE["contest-archive"])
        self.assertEqual(
            [item["link"] for item in items],
            ["/goi-contest-2014", "/halloween-contest"],
        )

    def test_international_uses_every_tab(self):
        items = parse_html(INTL_HTML, DATA_TYPE["scp-international"])
        self.assertEqual(items[0]["sub_scp_type"], "俄国分部-series")
        self.assertEqual(items[1]["link"], "/id-tale")
        self.assertEqual(items[1]["sub_scp_type"], "印尼分部-tale")

    def test_wander_library_links(self):
        items = parse_html(WANDER_LIBRARY_HTML, DATA_TYPE["wander-cn"])
        self.assertEqual([item["link"] for item in items], ["/wanderers:potions-introduction"])

    def test_pager_and_types(self):
        html = '<div class="pager"><span class="pager-no">page 1 of 3</span></div>'
        self.assertEqual(
            extra_page_urls("https://scp-wiki-cn.wikidot.com/tales-by-page-name", html),
            [
                "https://scp-wiki-cn.wikidot.com/tales-by-page-name/p/2",
                "https://scp-wiki-cn.wikidot.com/tales-by-page-name/p/3",
            ],
        )
        self.assertEqual(extra_page_urls("https://scp-wiki-cn.wikidot.com/tales-by-page-name/p/2", html), [])
        self.assertEqual(get_type_by_url("https://scp-wiki-cn.wikidot.com/scp-series-10"), DATA_TYPE["scp-series"])
        self.assertEqual(get_type_by_url("https://scp-wiki-cn.wikidot.com/scp-series-cn-5/p/2"), DATA_TYPE["scp-series-cn"])
        self.assertEqual(series_url("en", 1), "https://scp-wiki-cn.wikidot.com/scp-series")
        self.assertEqual(series_url("cn", 4), "https://scp-wiki-cn.wikidot.com/scp-series-cn-4")

    def test_child_links_and_upsert(self):
        html = '''
        <a href="/scp-173/offset/1">下一页</a>
        <a href="/fragment:scp-173-02">片段</a>
        <a href="/fragment:scp-1730-02">别人的片段</a>
        <a href="https://example.com/scp-173/offset/3">外站</a>
        '''
        self.assertEqual(
            child_links("/scp-173", html),
            ["/scp-173/offset/1", "/fragment:scp-173-02"],
        )
        self.assertEqual(normalize_link("https://scp-wiki-cn.wikidot.com/scp-173"), "/scp-173")

        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            con = sqlite3.connect(path)
            con.execute(
                '''CREATE TABLE scps(
                    _id INTEGER PRIMARY KEY AUTOINCREMENT,
                    _index INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    scp_type INTEGER NOT NULL,
                    author TEXT,
                    created_time TEXT,
                    sub_scp_type TEXT)'''
            )
            con.execute("CREATE UNIQUE INDEX idx_scps_link_type ON scps(link, scp_type)")
            con.execute(
                '''CREATE TABLE scp_detail(
                    link TEXT PRIMARY KEY,
                    not_found INTEGER,
                    detail TEXT,
                    tags TEXT)'''
            )
            item = parse_html(TALE_HTML, DATA_TYPE["tales-by-page-name"])[0]
            self.assertTrue(upsert_category(con.cursor(), item))
            item["title"] = "火之洗礼-修订"
            upsert_category(con.cursor(), item)
            row = con.execute("SELECT title, author, COUNT(*) FROM scps").fetchone()
            self.assertEqual(row[0], "火之洗礼-修订")
            self.assertEqual(row[1], "ahshow")
            self.assertEqual(row[2], 1)
            from scrapy_spider.items import ScpDetailItem
            upsert_detail(con.cursor(), ScpDetailItem(
                link="/a-baptism-of-fire", detail="<p>第一行\n第二行</p>", not_found=0, tags="tale"
            ))
            detail = con.execute("SELECT detail FROM scp_detail").fetchone()[0]
            self.assertIn("\n", detail)
            con.close()
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
