# -*- coding: utf-8 -*-
from MayhemCookiesHandler import MayhemCookiesHandler
from MayhemRequestHandler import MayhemRequestHandler
from MayhemCastingParser import MayhemCastingParser
from CastingLocationObject import CastingLocationObject
import pickle
import time
import sqlite3 as lite
from datetime import date

class MayhemMiner:
	def __init__(self, verbosity):
		self.verbosity = verbosity
		self.castingDataDict = {}
		self.browseDataDict = {}
		self.mine()
		
	def mine(self):
		page = MayhemCookiesHandler(self.verbosity)
		
		if page == -1:
			return -1
		elif page == -2:
			return -2
		else:
			totalLocation = self.loadLocation()
			processedLocation = 1
			
			for location in self.locationSet:
				if self.verbosity == 1:
					print "Launching request on", location.read(), "(", processedLocation, "of", totalLocation, "hotspots)"
				casting = MayhemRequestHandler("http://www.modelmayhem.com/casting/result/", page, self.verbosity)
				casting.launchCastingRequest(self.castingDataDict, location.getCountry(), location.getState())
				print
				browse = MayhemRequestHandler("http://www.modelmayhem.com/browse/results/", page, self.verbosity)
				browse.launchBrowseRequest(self.browseDataDict, location.getCountry(), location.getState())
				print
			
				if self.verbosity == 1:
					print len(self.castingDataDict), "casting,", len(self.browseDataDict), "members key-value pairs generated"
					#print len(self.browseDataDict), "browse key-value pairs generated"
					#print "Idle for 2 seconds..."
				time.sleep(2)
				processedLocation += 1
				
			output = open('castingSummary.pkl', 'wb')
			pickle.dump(self.castingDataDict, output)
			output.close()
			output = open('membersSummary.pkl', 'wb')
			pickle.dump(self.browseDataDict, output)
			output.close()
			
			# used for reversing dump above in case of db failure
			#f = open("castingSummary.pkl", 'r')
			#self.castingDataDict = pickle.load(f)
			#g = open("membersSummary.pkl", 'r')
			#self.browseDataDict = pickle.load(g)
			#self.loadToDB()
				
		#for k, v in sorted(self.castingDataDict.iteritems()):
		#	print k, v.dump()		
		return 0
		
	def loadToDB(self):
		runtime = date.today()
		formattedDate = str(runtime.year) + '-' + str(runtime.month) + '-' + str(runtime.day)
		connection = lite.connect('casting.db')
		connection.text_factory = str
		
		caster = list()
		seek = list()
		member = list()
		
		professionType = {"Model": 1,
						"Photographer": 2,
						"Makeup Artist": 3,
						"Hair Stylist": 4,
						"Wardrobe Stylist": 5,
						"Retoucher": 7,
						"Artist/Painter": 9,
						"Publication": 11,
						"Casting Director": 13,
						"Event Planner": 14,
						"Advertiser": 15,
						"Filmmaker": 16,
						"Film/TV Producer": 16,
						"Body Painter": 19,
						"Clothing Designer": 20,
						"Approved Agency": 23,
						"Digital Artist": 24,
						"Moderator": 98,
						"": 99}
		seekType = {"Female Models": 0,
						"Male Models": 1,
						"Photographer": 3,
						"Makeup Artist": 4,
						"Hair Stylist": 5,
						"Wardrobe Stylist": 6,
						"Retoucher": 8,
						"Artist/Painter": 9,
						"Body Painter": 10,
						"Publication": 11,
						"Filmmaker": 12,
						"Clothing Designer": 13,
						"Approved Agency": 14,
						"Digital Artist": 15,
						"": 99}
						
		for k, v in (self.browseDataDict.iteritems()):
			member.append((k, professionType[v.profession], v.town, v.state, v.country, v.gender, v.lastActivity, v.shootNudes, v.compensation, v.experience))
		for k, v in (self.castingDataDict.iteritems()):
			# Nudity: both will be marked as 1, same as nudity: yes. Nudity: no marked as 0.
			# Keep it simple!
			caster.append((k, professionType[v.profession], v.town, v.state, v.country, 0 if v.nudity == "No" else 1, v.compensation, formattedDate))
			for s in v.seeking:
				seek.append((k, seekType[s], formattedDate))
		with connection:
			for mq in member:
				connection.execute("INSERT OR REPLACE INTO Member (MID, Profession, Town, State, Country, Gender, LastActivity, ShootNudes, Compensation, Experience)\
									VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", mq)
			for cq in caster:
				#print cq
				connection.execute("INSERT INTO Caster (ID, Profession, Town, State, Country, Nudity, Compensation, Runtime)\
									VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cq)
			
			for sq in seek:
				connection.execute("INSERT INTO Seek (ID, Seeking, Runtime) VALUES (?, ?, ?)", sq)
		
	def loadLocation(self):
		self.locationSet = set()
		self.locationSet.add(CastingLocationObject('CA', "Alberta", 7532))
		self.locationSet.add(CastingLocationObject('CA', "British Columbia", 7529))
		self.locationSet.add(CastingLocationObject('CA', "Manitoba", 7535))
		self.locationSet.add(CastingLocationObject('CA', "New Brunswick", 7539))
		self.locationSet.add(CastingLocationObject('CA', "Newfoundland and Labrador", 7537))
		self.locationSet.add(CastingLocationObject('CA', "Northwest Territories", 7533))
		self.locationSet.add(CastingLocationObject('CA', "Nova Scotia", 7536))
		self.locationSet.add(CastingLocationObject('CA', "Nunavut", 7540))
		self.locationSet.add(CastingLocationObject('CA', "Ontario", 7530))
		self.locationSet.add(CastingLocationObject('CA', "Prince Edward Island", 7534))
		self.locationSet.add(CastingLocationObject('CA', "Quebec", 7531))
		self.locationSet.add(CastingLocationObject('CA', "Saskatchewan", 7538))
		self.locationSet.add(CastingLocationObject('CA', "Yukon", 7541))
		
		self.locationSet.add(CastingLocationObject('US', "Alabama", 4078))
		self.locationSet.add(CastingLocationObject('US', "Alaska", 4079))
		self.locationSet.add(CastingLocationObject('US', "Arizona", 4080))
		self.locationSet.add(CastingLocationObject('US', "Arkansas", 4081))
		self.locationSet.add(CastingLocationObject('US', "California", 4082))
		self.locationSet.add(CastingLocationObject('US', "Colorado", 4087))
		self.locationSet.add(CastingLocationObject('US', "Connecticut", 4088))
		self.locationSet.add(CastingLocationObject('US', "Delaware", 4089))
		self.locationSet.add(CastingLocationObject('US', "District of Columbia", 4090))
		self.locationSet.add(CastingLocationObject('US', "Florida", 4091))
		self.locationSet.add(CastingLocationObject('US', "Georgia", 4092))
		self.locationSet.add(CastingLocationObject('US', "Guam", 8049))
		self.locationSet.add(CastingLocationObject('US', "Hawaii", 4093))
		self.locationSet.add(CastingLocationObject('US', "Idaho", 4094))
		self.locationSet.add(CastingLocationObject('US', "Illinois", 4095))
		self.locationSet.add(CastingLocationObject('US', "Indiana", 4096))
		self.locationSet.add(CastingLocationObject('US', "Iowa", 4097))
		self.locationSet.add(CastingLocationObject('US', "Kansas", 4098))
		self.locationSet.add(CastingLocationObject('US', "Kentucky", 4099))
		self.locationSet.add(CastingLocationObject('US', "Louisiana", 4100))
		self.locationSet.add(CastingLocationObject('US', "Maine", 4101))
		self.locationSet.add(CastingLocationObject('US', "Maryland", 4102))
		self.locationSet.add(CastingLocationObject('US', "Massachusetts", 4103))
		self.locationSet.add(CastingLocationObject('US', "Michigan", 4104))
		self.locationSet.add(CastingLocationObject('US', "Minnesota", 4105))
		self.locationSet.add(CastingLocationObject('US', "Mississippi", 4106))
		self.locationSet.add(CastingLocationObject('US', "Missouri", 4107))
		self.locationSet.add(CastingLocationObject('US', "Montana", 4108))
		self.locationSet.add(CastingLocationObject('US', "Nebraska", 4109))
		self.locationSet.add(CastingLocationObject('US', "Nevada", 4110))
		self.locationSet.add(CastingLocationObject('US', "New Hampshire", 4111))
		self.locationSet.add(CastingLocationObject('US', "New Jersey", 4112))
		self.locationSet.add(CastingLocationObject('US', "New Mexico", 4113))
		self.locationSet.add(CastingLocationObject('US', "New York", 4114))
		self.locationSet.add(CastingLocationObject('US', "North Carolina", 4115))
		self.locationSet.add(CastingLocationObject('US', "North Dakota", 4116))
		self.locationSet.add(CastingLocationObject('US', "Ohio", 4117))
		self.locationSet.add(CastingLocationObject('US', "Oklahoma", 4118))
		self.locationSet.add(CastingLocationObject('US', "Oregon", 4119))
		self.locationSet.add(CastingLocationObject('US', "Pennsylvania", 4120))
		self.locationSet.add(CastingLocationObject('US', "Puerto Rico", 8058))
		self.locationSet.add(CastingLocationObject('US', "Rhode Island", 4121))
		self.locationSet.add(CastingLocationObject('US', "South Carolina", 4122))
		self.locationSet.add(CastingLocationObject('US', "South Dakota", 4123))
		self.locationSet.add(CastingLocationObject('US', "Tennessee", 4124))
		self.locationSet.add(CastingLocationObject('US', "Texas", 4125))
		self.locationSet.add(CastingLocationObject('US', "Utah", 4126))
		self.locationSet.add(CastingLocationObject('US', "Vermont", 4132))
		self.locationSet.add(CastingLocationObject('US', "Virgina", 4127))
		self.locationSet.add(CastingLocationObject('US', "Virgin Islands", 8059))
		self.locationSet.add(CastingLocationObject('US', "Washington", 4128))
		self.locationSet.add(CastingLocationObject('US', "Washington DC", 8056))
		self.locationSet.add(CastingLocationObject('US', "West Virgina", 4129))
		self.locationSet.add(CastingLocationObject('US', "Wisconsin", 4130))
		self.locationSet.add(CastingLocationObject('US', "Wyoming", 4131))

		return len(self.locationSet)
