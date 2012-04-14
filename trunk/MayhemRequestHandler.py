# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2
import re
import sys
from MayhemCastingParser import MayhemCastingParser

class MayhemRequestHandler:
	def __init__(self, URL, page, verbosity):
		self.URL = URL
		self.page = page
		self.result = None
		self.successStringSearch = "Displaying results"
		self.multiplePagesSearch = "thepagenums"
		self.pageCount = 0
		self.currentPage = 1
		self.pageModulus = 50
		self.verbosity = verbosity
		self.castingParser = MayhemCastingParser(self.verbosity)
		
	def launchRequest(self, castingDataDict, stateID, townID):		
		params = urllib.urlencode([('fm_action', "Search")
									, ('search_type', "casting for")
									, ('m_search_type[]', "0")
									, ('m_search_type[]', "1")
									, ('m_search_type[]', "3")
									, ('m_search_type[]', "4")
									, ('m_search_type[]', "5")
									, ('m_search_type[]', "6")
									, ('m_search_type[]', "8")
									, ('m_search_type[]', "9")
									, ('m_search_type[]', "10")
									, ('m_search_type[]', "11")
									, ('m_search_type[]', "12")
									, ('m_search_type[]', "13")
									, ('m_search_type[]', "14")
									, ('m_search_type[]', "15")
									, ('cc_country', "US")
									, ('cc_state', stateID)
									, ('cc_city', townID)
									, ('search_mile_range', "1.00")
									, ('fm_button', " ")
									, ('search_start_date', "")
									, ('search_end_date', "")
									, ('search_include_cc', "cc")
									, ('c_compensation_amount', "")
									, ('search_keyword', "")
									, ('search_mm_id', "")])

		while True:
			t = self.page.opener.open(self.URL + str(self.currentPage) + '/?' + params)
			self.result = t.read()
			
			if re.search(self.successStringSearch, self.result) != None:
				# Only need to be checked once to get number of pages
				if self.pageCount == 0:
					if re.search(self.multiplePagesSearch, self.result) != None:
						self.countNumberOfPages(self.verbosity)
					else:
						self.pageCount = 1
						
				if self.verbosity >= 2:
					print self.URL + params
					print self.result
					
				if self.verbosity >= 1:
					print "Page", self.currentPage, "of", self.pageCount, ":" \
						, sys.getsizeof(self.result), "bytes returned"
					
			self.castingParser.parse(castingDataDict, self.result)
			if self.currentPage == self.pageCount:
				break
			else:
				self.currentPage += 1
				
	def countNumberOfPages(self, verbosity):
		resultCount = re.search(".(results )[0-9\-]+[ ]+(of)[ ]+([0-9]+)", self.result)
		self.pageCount = int(resultCount.group(3)) / self.pageModulus + 1
		if verbosity == 1:
			print self.pageCount, "pages to search"
