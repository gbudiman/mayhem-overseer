# -*- coding: utf-8 -*-
from MayhemCookiesHandler import MayhemCookiesHandler
from MayhemRequestHandler import MayhemRequestHandler
from MayhemCastingParser import MayhemCastingParser

class MayhemMiner:
	def __init__(self, verbosity):
		self.verbosity = verbosity
		self.castingDataDict = {}
		self.mine()
		
	def mine(self):
		page = MayhemCookiesHandler(self.verbosity)
		
		if page == -1:
			return -1
		elif page == -2:
			return -2
		else:
			request = MayhemRequestHandler("http://www.modelmayhem.com/casting/result/", page, self.verbosity)
			request.launchRequest(self.castingDataDict)
			for k, v in sorted(self.castingDataDict.iteritems()):
				print k, v.dump()
			
		return 0