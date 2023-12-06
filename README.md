# SCP-Spider

[SCP基金会](http://scp-wiki-cn.wikidot.com)的爬虫工具，主要用于app的数据更新
依赖scrapy进行抓取，主要步骤：
- 抓取需要的页面和条目目录，写入数据库
- 从数据库取到url批量抓取正文内容，写入数据库
