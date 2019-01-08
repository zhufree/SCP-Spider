# SCP-Spider

[SCP基金会](http://scp-wiki-cn.wikidot.com)的爬虫工具，主要用于app的数据更新
依赖scrapy进行抓取，主要步骤：
- 抓取需要的页面和条目目录，写入数据库
- 从数据库取到url批量抓取正文内容，写入数据库

目前已完成scp系列和scp-cn系列的重构

TODO：
- [x] TALE
- [x] ARCHIVES
- Collections
    - [ ] 故事系列
    - [ ] 设定中心
    - [ ] 征文竞赛
- 补充内容（不作为目录）
    - [x] 事故记录
    - [ ] offset
- [ ] 正文


添加新模块：
- 在constants中添加抓取链接，添加新的scp_type类型
- 观察页面元素创建或选择合适的item
- 添加以下步骤：
    - 根据url判断scp_type
    - 根据scp_type抓取内容
    - 根据item type处理数据库插入