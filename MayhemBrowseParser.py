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
		
		print len(profession)
		print len(location)
		iLocation = iter(location)
		for d in profession:
			print d
		for d in location:
			print d
