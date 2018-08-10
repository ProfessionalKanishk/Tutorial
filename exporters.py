from scrapy.exporters import JsonLinesItemExporter
from WebScraper.items import jsonItem

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