# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2

class MayhemRequestHandler:
	def __init__(self, URL, page):
		self.URL = URL
		self.page = page
		
	def launchRequest(self, index=1):		
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
									, ('cc_state', "4093")
									, ('cc_city', "2740281")
									, ('search_mile_range', "1.00")
									, ('fm_button', " ")
									, ('search_start_date', "")
									, ('search_end_date', "")
									, ('search_include_cc', "cc")
									, ('c_compensation_amount', "")
									, ('search_keyword', "")
									, ('search_mm_id', "")])

		t = self.page.opener.open(self.URL + params)
		print t.read()
