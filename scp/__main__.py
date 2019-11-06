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
# c.crawl_main_list()
# c.crawl_single_pages()
# c.crawl_collection_pages()
# c.set_download_type() # 在offset之前设置download type，然后据此分块抓offset
# c.crawl_offset_pages()
c.crawl_main_detail()
# c.set_download_type() # offset抓完之后给offset也设置download_type
# c.split_csv()
