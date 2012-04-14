# -*- coding: utf-8 -*-
from MayhemCookiesHandler import MayhemCookiesHandler
from MayhemRequestHandler import MayhemRequestHandler
from MayhemCastingParser import MayhemCastingParser
from CastingLocationObject import CastingLocationObject

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
			self.loadLocation()
			for location in self.locationSet:
				if self.verbosity == 1:
					print "Launching request on", location.read()
				request = MayhemRequestHandler("http://www.modelmayhem.com/casting/result/", page, self.verbosity)
				request.launchRequest(self.castingDataDict, location.getState(), location.getTown())
			#for k, v in sorted(self.castingDataDict.iteritems()):
			#	print k, v.dump()
			
		return 0
		
	def loadLocation(self):
		self.locationSet = set()
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Hilo", 2740241))
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Honolulu", 2740281))