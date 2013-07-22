# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.spider import BaseSpider
class DmozSpider(BaseSpider):
  name = 'dmoz'
  allowed_domains = ['dmoz.org']
  