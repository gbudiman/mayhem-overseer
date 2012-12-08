# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib
import urllib
import urllib2
import re
import sys
from MayhemCastingParser import MayhemCastingParser
from MayhemBrowseParser import MayhemBrowseParser
import time
from decimal import *

class MayhemRequestHandler:
	def __init__(self, URL, page, verbosity):
		self.URL = URL
		self.page = page
		self.result = None
		self.successStringSearch = "Displaying results"
		self.multiplePagesSearch = "thepagenums"
		self.pageCount = 0
		self.currentPage = 1
		self.verbosity = verbosity
		self.castingParser = MayhemCastingParser(self.verbosity)
		self.terminalString = ''
		getcontext().prec = 4
		
	def animateTerminal(self, title, count):
		try:
			repeatCount = int(float(self.currentPage) / float(self.pageCount) * 32.0)
		except ZeroDivisionError:
			repeatCount  = 32
		whiteSpace = 32 - repeatCount
		sys.stdout.write('\b' * (len(self.terminalString) - 12))
		sys.stdout.flush()
		self.terminalString = ''
		if title == 'Members':
			self.terminalString += '\x1B[01;36m'
		elif title == 'Casting':
			self.terminalString += '\x1B[01;33m'
		self.terminalString += title + ' [' + '=' * repeatCount + '>' + ' ' * whiteSpace + '] '
		self.terminalString += str(self.currentPage) + '/' + str(self.pageCount) + ' (' + str(count) + ')'
		self.terminalString += ' ' + str(self.dataTransferred) + ' MB'
		self.terminalString += '\x1B[0m'
		sys.stdout.write(self.terminalString)
		sys.stdout.flush()
		
	def launchAnnounceRequest(self, message):
		params = urllib.urlencode([('announcement', message)
									, ('action', 'announcement')
									, ('vip_status', '')
									, ('submit', "Let's do this ALREADY!")])
		t = self.page.opener.open(self.URL, params)
		return t.read()
		
	def launchBrowseRequest(self, browseDataDict, countryID, stateID):
		self.membersParser = MayhemBrowseParser(self.verbosity)
		self.pageModulus = 40
		self.dataTransferred = Decimal(0)
		itemCount = 0
		params = urllib.urlencode([('fm_action', "search")
									, ('artist_type[]', '')
									, ('display', 'details')
									, ('sort_by', '2')
									, ('show_advanced', '1')
									, ('logged_days', '2') # speed up query being run daily
									, ('country', countryID)
									, ('state', stateID)
									, ('city', '')
									, ('toggle_counter', '6')])
									
		while True:
			try:
				t = self.page.opener.open(self.URL + str(self.currentPage) + '/?' + params, '', 10)
				#print self.URL + str(self.currentPage) + '/?' + params
			except:
				print("!!! Timeout. Retrying in 5 seconds...")
				time.sleep(5)
				continue
			self.result = t.read()
			
			if re.search(self.successStringSearch, self.result) != None:
				if self.pageCount == 0:
					self.countNumberOfPages(self.verbosity)
				
				if self.verbosity >= 2:
					print(self.URL + params)
					print(self.result)
					
				#if self.verbosity >= 1:
				#	print "Page", self.currentPage, "of", self.pageCount, ":" \
				#		, sys.getsizeof(self.result)/1024, "KB returned"
				self.dataTransferred += Decimal(sys.getsizeof(self.result))/1024/1024
						
			browseCount = self.membersParser.parse(browseDataDict, self.result)
			itemCount += browseCount
			self.animateTerminal("Members", itemCount)
			if self.currentPage == self.pageCount or browseCount <= 0:
				break
			else:
				self.currentPage += 1	
				
		return self.dataTransferred
		
	def launchCastingRequest(self, castingDataDict, countryID, stateID):	
		self.castingParser = MayhemCastingParser(self.verbosity)
		self.pageModulus = 50
		self.dataTransferred = Decimal(0)
		itemCount = 0
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
									, ('cc_country', countryID)
									, ('cc_state', stateID)
									, ('cc_city', '')
									, ('search_mile_range', '')
									, ('fm_button', " ")
									, ('search_start_date', "")
									, ('search_end_date', "")
									, ('search_include_cc', "cc")
									, ('c_compensation_amount', "")
									, ('search_keyword', "")
									, ('search_mm_id', "")])

		while True:
			try:
				t = self.page.opener.open(self.URL + str(self.currentPage) + '/?' + params, '', 10)
			except:
				print("!!! Timeout. Retrying in 5 seconds...")
				time.sleep(5)
				continue
			self.result = t.read()
			
			if re.search(self.successStringSearch, self.result) != None:
				# Only need to be checked once to get number of pages
				if self.pageCount == 0:
					self.countNumberOfPages(self.verbosity)
						
				if self.verbosity >= 2:
					print(self.URL + params)
					print(self.result)
					
				#if self.verbosity >= 1:
				#	print "Page", self.currentPage, "of", self.pageCount, ":" \
				#		, sys.getsizeof(self.result)/1024, "KB returned"
				self.dataTransferred += Decimal(sys.getsizeof(self.result))/1024/1024
					
			castingCount = self.castingParser.parse(castingDataDict, self.result)
			itemCount += castingCount
			self.animateTerminal("Casting", itemCount)
			if self.currentPage == self.pageCount or castingCount <= 0:
				break
			else:
				self.currentPage += 1
				
		return self.dataTransferred
				
	def countNumberOfPages(self, verbosity):
		resultCount = re.search(".(results )[0-9\- ]+[ ]+(of)[ ]+([0-9]+)", self.result)
		self.pageCount = (int(resultCount.group(3)) - 1) / self.pageModulus + 1
		#if verbosity == 1:
		#	print(self.pageCount, "pages to search")
