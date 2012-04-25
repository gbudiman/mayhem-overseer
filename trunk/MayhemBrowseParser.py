# -*- coding: utf-8 -*-
import re
import sys
import string
from MayhemCastingParser import MayhemCastingParser

class MayhemBrowseParser(MayhemCastingParser):
	def __init__(self, verbosity):
		super(MayhemBrowseParser, self).__init__(verbosity)
		
	def parse(self, dataDict, result):
		profession = re.findall("[\"][>]([A-Z a-z/]*)</div>[\n\r\t]+(?:</td>)", result)
		location = re.findall("([A-Z \'\-a-z]+)[,][ ]([A-Z \'\-a-z]+)[,][ ]([A-Z \'\-a-z]+)[\t]+(?:</td>)", result)
		gender = re.findall("(?:data1\">)([FeMmalen/]+)", result)
		lastActivity = re.findall("([A-Za-z.]+)[ ]([0-9]{1,2})[,][ ]([0-9]{4})", result)
		#additionalLocation = re.findall
		
		print len(profession)
		print len(location)
		print len(gender)
		print len(lastActivity)
		iLocation = iter(location)
		iGender = iter(gender)
		iLastActivity = iter(lastActivity)
		for d in profession:
			print d, iLocation.next(), iGender.next(), iLastActivity.next()