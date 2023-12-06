from .core import init_database, crawl_this_spider
import sys

# 2023.12.6 last update category
# python -m scp main
# category = main + single
# detail = detail + offset
options = sys.argv[1:]
init_database()
if not {'main', 'single', 'offset', 'detail', 'test'} & set(options):
    print('Please provide an option')
    sys.exit(0)
else:
    crawl_this_spider(options[0])

