# -*- coding: utf-8 -*-
from MayhemCookiesHandler import MayhemCookiesHandler
from MayhemRequestHandler import MayhemRequestHandler
from MayhemCastingParser import MayhemCastingParser
from CastingLocationObject import CastingLocationObject
import pickle

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
				if self.verbosity == 1:
					print len(self.castingDataDict), "key-value pairs generated"
			
			output = open('castingSummary.pkl', 'wb')
			pickle.dump(self.castingDataDict, output)
			output.close()
		return 0
		
	def loadLocation(self):
		self.locationSet = set()
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Anchorage", 2734619))
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Fairbanks", 2734698))
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Juneau", 2734744))
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Hilo", 2740241))
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Honolulu", 2740281))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Kennewick", 2759815))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Seattle", 2759999))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Spokane", 2760234))
