# -*- coding: utf-8 -*-

from .core import ScpSpider
#
# # options = sys.argv[1:]
# # if not {'news', 'follow'} & set(options):
# #     print('Please provide a notification option: "news" or "follow"')
# #     sys.exit(0)
#
# if __name__ == '__main__':
c = ScpSpider()
c.crawl_main_list()
# c.crawl_main_detail()
