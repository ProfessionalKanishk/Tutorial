# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import errno
from scrapy.pipelines.files import FilesPipeline
from scrapy.exporters import JsonLinesItemExporter
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
			print(item['pdfURL'])
			print(type(item['pdfURL']))
			request = Request(url=item['pdfURL'])
			request.meta['file_dir'] = item['caseName']+'\\'+item['fileName']
			yield request
			
	def file_path(self, request, response=None, info=None):
	
		if not isinstance(item, WebscraperItem):
			return item
		FILES_STORE = 'D:\\Documents\\Job\\WebScraper'
		filename = request.url.split('/')[-1]
		filename = filename[:50].rstrip()
		filedir = request.meta['file_dir']
		filepath = FILES_STORE+'\\'+filedir + '\\' + filename		
		return filepath
		
	
class jsonItemExporter(JsonLinesItemExporter):

	def __init__(self, file, **kwargs):
		self._configure(kwargs)
		self.file = file
		self.encoder = json.JSONEncoder(**kwargs)
		self.first_item = True

	def start_exporting(self):
		self.file.write("[")

	def finish_exporting(self):
		self.file.write("]")

	def export_item(self, item):
		if not isinstance(item, jsonItem):
			return item
		if self.first_item:
			self.first_item = False
		else:
			self.file.write(',\n')
		itemdict = dict(self._get_serialized_fields(item))
		self.file.write(self.encoder.encode(itemdict))