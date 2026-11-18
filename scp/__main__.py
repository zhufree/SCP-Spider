from .core import init_database, crawl_this_spider
import sys

# python -m scp main
# python -m scp single
# python -m scp detail
# python -m scp offset
options = sys.argv[1:]
init_database()
if not {'main', 'single', 'offset', 'detail', 'test'} & set(options):
    print('Please provide an option')
    sys.exit(0)
else:
    crawl_this_spider(options[0])

