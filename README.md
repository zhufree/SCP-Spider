# SCP-Spider

[SCP基金会](https://scp-wiki-cn.wikidot.com)的爬虫工具，主要用于 app 的数据更新。依赖 Scrapy 和 PyQuery。

数据库写在项目下的 `data/`：

- `data/scp_category_v2.db`：目录
- `data/scp_detail_v2.db`：正文

在仓库根目录执行：

```
python -m scp main      # 目录。系列页数和 /p/N 跟当前站点走，遇到 404 停止
python -m scp single    # 单页（异常物品、三句话外围等会跟着分页）
python -m scp detail    # 补正文，并顺着文内的 /offset/ 与 fragment: 链接继续抓
python -m scp offset    # 从已保存的正文里再补一轮 offset / fragment
```

同一 `link + scp_type` 会覆盖更新，重复跑不会插出第二行。请求有下载间隔和 AutoThrottle。
