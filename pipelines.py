# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import errno
import json
from scrapy.pipelines.files import FilesPipeline
from WebScraper.items import WebscraperItem
from WebScraper.items import jsonItem
from scrapy import Request
import urllib
import time


class WebscraperPipeline(FilesPipeline):
	def get_media_requests(self,item,info):
	
		if not isinstance(item, WebscraperItem):
			return item
			
			
		if 'pdfURL' in item:
			request = Request(url=item['pdfURL'])
			request.meta['file_dir'] = item['caseName']+'\\'+item['fileName']
			yield request
			
	def file_path(self, request, response=None, info=None):
	
		FILES_STORE = 'D:\\Documents\\Job\\WebScraper\\PDF'
		filename = request.url.split('/')[-1]
		filename = filename[:50].rstrip()
		filedir = request.meta['file_dir']
		filepath = FILES_STORE+'\\'+filedir + '\\' + filename	

		return filepath
		
	
class jsonPipeline(object):

	def open_spider(self, spider):
		self.file = open('NotData.json', 'w')
		self.file.write("[")

	def close_spider(self, spider):
		self.file.write("]")
		self.file.close()

	def process_item(self, item, spider):
		if not isinstance(item, jsonItem):
			return item
			
		
		line = json.dumps(
			dict(item),
			sort_keys=False,
			indent=4,
			separators=(',', ': ')
		) + ",\n"

		self.file.write(line)
		return item