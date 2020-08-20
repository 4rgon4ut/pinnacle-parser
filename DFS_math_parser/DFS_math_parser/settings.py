
# Scrapy settings for DFS_math_parser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'DFS_math_parser'

SPIDER_MODULES = ['DFS_math_parser.spiders']
NEWSPIDER_MODULE = 'DFS_math_parser.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}


# TODO: Set DB connection details

DATABASE_SETTINGS = {
    'database': '',
    'user': '',
    'password': '',
}


# TODO: Set proxy settings

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the setting
PROXY_MODE = 2

CUSTOM_PROXY = ""

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
# PROXY_LIST = '/home/n30n/Run/DFS_math/DFS_math_parser/DFS_math_parser/proxy'

RETRY_TIMES = 10

RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]