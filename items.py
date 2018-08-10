# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	pdfURL = scrapy.Field()
	caseName = scrapy.Field()
	fileName = scrapy.Field()

	
class jsonItem(scrapy.Item):
    # define the fields for your item here like:
	caseName = scrapy.Field()
	files = scrapy.Field()