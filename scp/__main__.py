# -*- coding: utf-8 -*-

from .core import init_database, crawl_this_spider
import sys

# 2021.12.12 last update category and detail
# python -m scp main
# category = main + single
options = sys.argv[1:]
init_database()
if not {'main', 'single', 'offset', 'collection_list', 'detail', 'test'} & set(options):
    print('Please provide an option')
    sys.exit(0)
else:
    crawl_this_spider(options[0])

