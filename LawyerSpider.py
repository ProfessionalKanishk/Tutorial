#Question: Figure out how to sort out the PDF files which are scraped.
from __future__ import absolute_import

import scrapy
import os
import errno
import re

from WebScraper.items import WebscraperItem
from WebScraper.items import jsonItem

from scrapy.http import Request

class LawyerSpider(scrapy.Spider):


	name = "Lawyer"
	allowed_domains = ['italaw.com']
	start_urls = ['https://www.italaw.com/cases/3826']
	
	caseCounter = 0
	caseList={}

	def parse(self, response):
	
		
		#Extracting the title of case
		try:
			item = WebscraperItem()
			newCase = jsonItem()
			title = response.selector.xpath('//h1[@id="page-title"]//text()').extract()
			caseURL = str(response.request.url)
			caseNum = caseURL.split("/cases/")[1]
			print("CaseNum: "+caseNum)
			if title[0].strip():
				item['caseName']=title[0]
				newCase['caseName']=title[0]
			else:
				item['caseName']=caseNum
				newCase['caseName']=caseNum
				
				
			stripped_text = ''
			for c in item['caseName']:
				   stripped_text += c if len(c.encode(encoding='utf_8'))==1 else ''		
			item['caseName'] = stripped_text
			item['caseName'] = item['caseName'].strip()[:70].rstrip()
				
			fileCounter = 1
			files=[]
			while fileCounter<20:
				fileName1 = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]/div[contains(@class,"views-field views-field-field-case-doc-file")]//text()'.format(fileCounter)).extract()
				fileName2 = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]/div[contains(@class,"views-field views-field-field-case-document-no-pdf-")]//text()'.format(fileCounter)).extract()
				if fileName1 == [] and fileName2 == []:
					try:
						fileName1 = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]/div[contains(@class,"views-field views-field-field-document-related-link")]//text()'.format(fileCounter)).extract()
						if not fileName1:
							raise Exception("No File Found")
					except:
						break
				fileName = ""
				for n in fileName1+fileName2:
					fileName += n	
				fileName = " ".join(fileName.split())
				if not fileName:
					fileName = "File "+str(fileCounter)
					
				print("File Name: "+fileName)
				item['fileName']=fileName
				stripped_text = ''
				for c in item['fileName']:
				   stripped_text += c if len(c.encode(encoding='utf_8'))==1 else ''		
				item['fileName'] = stripped_text
				item['fileName'] = item['fileName'].strip()[:80].rstrip()
				
				
				file={}												#Formats for file in JSON
				file['Name Of Document']=fileName
				try:
					day = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]/div/div/span[@class="day"]//text()'.format(fileCounter)).extract()
					monthYear = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//span[@class="month-year"]//text()'.format(fileCounter)).extract()
					file['Date']=day[0]+" "+monthYear[0]
				except:
					pass
				try:
					claimant = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="views-field" and span[contains(text(),"Claimant appointee")]]/div[@class="field-content"]//text()'.format(fileCounter)).extract()
					claimant = " ".join(claimant)
					if claimant:
						file['Claimant Respondent']=claimant
				except:
					pass
				try:
					respondent = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="views-field" and span[contains(text(),"Respondent appointee")]]/div[@class="field-content"]//text()'.format(fileCounter)).extract()
					respondent = " ".join(respondent)
					if respondent:
						file['Respondent']=respondent
				except:
					pass
				try:
					arbitrator = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="views-field" and span[contains(text(),"Arbitrator(s)")]]/div[@class="field-content"]//text()'.format(fileCounter)).extract()
					arbitrator = " ".join(arbitrator)
					if arbitrator:
						file['Arbitrator']=arbitrator
				except:
					pass
				try:
					president = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="views-field" and span[contains(text(),"Chair/President")]]/div[@class="field-content"]//text()'.format(fileCounter)).extract()
					president = " ".join(president)
					if president:
						file['Chair/President']=president
				except:
					pass
				try:
					counsel = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="views-field" and span[contains(text(),"Claimant\'s counsel")]]/div[@class="field-content"]//text()'.format(fileCounter)).extract()
					counsel = " ".join(counsel)
					if counsel:
						file['Claimant\'s Counsel']=counsel
				except:
					pass
					
					
				files.append(file)
				
				try:
					pdfURLs = response.selector.xpath('//div[contains(@class,"views-row views-row-{}")]//div[@class="item-list"]//a[@href]/@href'.format(fileCounter)).extract()
					for pdfURL in pdfURLs:
						if pdfURL.endswith('.pdf'):
							item['pdfURL']=pdfURL
							#yield item
				except Exception as e:
					print(e)
					
				fileCounter += 1
				
			newCase['files']=files
			print(newCase['files'])
			print(newCase)
			yield newCase
			
		except Exception as e:
			print(e)
