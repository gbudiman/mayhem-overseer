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
				request = MayhemRequestHandler("http://www.modelmayhem.com/casting/result/", page, self.verbosity)
				request.launchRequest(self.castingDataDict, location.getState(), location.getTown())
			
				if self.verbosity == 1:
					print len(self.castingDataDict), "key-value pairs generated"
					print "Idle for 5 seconds..."
				time.sleep(5)
				processedLocation += 1
				
			output = open('castingSummary.pkl', 'wb')
			pickle.dump(self.castingDataDict, output)
			output.close()
			self.loadToDB()
					
			#for k, v in sorted(self.castingDataDict.iteritems()):
			#	print k, v.dump()		
		return 0
		
	def loadToDB(self):
		runtime = date.today()
		formattedDate = str(runtime.year) + '-' + str(runtime.month) + '-' + str(runtime.day)
		connection = lite.connect('casting.db')
		
		caster = list()
		seek = list()
		
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
						"Body Painter": 19,
						"Clothing Designer": 20,
						"Approved Agency": 23,
						"Digital Artist": 24,
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
						
		for k, v in (self.castingDataDict.iteritems()):
			caster.append((k, professionType[v.profession], v.town, v.state, 0 if v.nudity == "No" else 1, v.compensation, formattedDate))
			for s in v.seeking:
				seek.append((k, seekType[s], formattedDate))
		with connection:
			for cq in caster:
				#print cq
				connection.execute("INSERT INTO Caster (ID, Profession, Town, State, Nudity, Compensation, Runtime)\
									VALUES (?, ?, ?, ?, ?, ?, ?)", cq)
			
			for sq in seek:
				connection.execute("INSERT INTO Seek (ID, Seeking, Runtime) VALUES (?, ?, ?)", sq)
		
	def loadLocation(self):
		self.locationSet = set()
		self.locationSet.add(CastingLocationObject("Alabama", 4078, "Auburn", 2734130))
		self.locationSet.add(CastingLocationObject("Alabama", 4078, "Huntsville", 2734336))
		self.locationSet.add(CastingLocationObject("Alabama", 4078, "Mobile", 2734409))
		self.locationSet.add(CastingLocationObject("Alabama", 4078, "Tuscaloosa", 2734565))
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Anchorage", 2734619))
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Fairbanks", 2734698))
		self.locationSet.add(CastingLocationObject("Alaska", 4079, "Juneau", 2734744))
		self.locationSet.add(CastingLocationObject("Arizona", 4080, "Lake Havasu City", 2735056))
		self.locationSet.add(CastingLocationObject("Arizona", 4080, "Phoenix", 2735098))
		self.locationSet.add(CastingLocationObject("Arizona", 4080, "Tucson", 2735177))
		self.locationSet.add(CastingLocationObject("Arizona", 4080, "Winslow", 2735195))
		self.locationSet.add(CastingLocationObject("Arkansas", 4081, "Benton", 2735237))
		self.locationSet.add(CastingLocationObject("Arkansas", 4081, "Jonesboro", 2735457))
		self.locationSet.add(CastingLocationObject("California", 4082, "Chico", 2735887))
		self.locationSet.add(CastingLocationObject("California", 4082, "Delano", 2735954))
		self.locationSet.add(CastingLocationObject("California", 4082, "Fortuna", 2736058))
		self.locationSet.add(CastingLocationObject("California", 4082, "Riverside", 2736517))
		self.locationSet.add(CastingLocationObject("California", 4082, "Santa Cruz", 2736584))
		self.locationSet.add(CastingLocationObject("Colorado", 4087, "Montrose", 2738387))
		self.locationSet.add(CastingLocationObject("Colorado", 4087, "Parker", 2738419))
		self.locationSet.add(CastingLocationObject("Colorado", 4087, "Sterling", 2738472))
		self.locationSet.add(CastingLocationObject("Colorado", 4087, "Trinidad", 2738487))
		self.locationSet.add(CastingLocationObject("Connecticut", 4088, "Danbury", 2738540))
		#self.locationSet.add(CastingLocationObject("Delaware", 4089, "", x))
		#self.locationSet.add(CastingLocationObject("District of Columbia", 4090, "", x))
		self.locationSet.add(CastingLocationObject("Florida", 4091, "Jacksonville", 2738941))
		self.locationSet.add(CastingLocationObject("Florida", 4091, "Lakeland", 2739504))
		self.locationSet.add(CastingLocationObject("Florida", 4091, "Panama City", 2738768))
		self.locationSet.add(CastingLocationObject("Florida", 4091, "Weston", 2738878))
		self.locationSet.add(CastingLocationObject("Georgia", 4092, "Albany", 2739831))
		self.locationSet.add(CastingLocationObject("Georgia", 4092, "Alpharetta", 2739875))
		self.locationSet.add(CastingLocationObject("Georgia", 4092, "Savannah", 2739719))
		#self.locationSet.add(CastingLocationObject("Guam", 8049, "", x))
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Hilo", 2740241))
		self.locationSet.add(CastingLocationObject("Hawaii", 4093, "Honolulu", 2740281))
		self.locationSet.add(CastingLocationObject("Idaho", 4094, "Rexburg", 2740518))
		self.locationSet.add(CastingLocationObject("Idaho", 4094, "Twin Falls", 2740556))
		self.locationSet.add(CastingLocationObject("Illinois", 4095, "Joliet", 2741826))
		self.locationSet.add(CastingLocationObject("Illinois", 4095, "Springfield", 2741680))
		self.locationSet.add(CastingLocationObject("Indiana", 4096, "Indianapolis", 2742224))
		self.locationSet.add(CastingLocationObject("Iowa", 4097, "Davenport", 2743248))
		self.locationSet.add(CastingLocationObject("Iowa", 4097, "Des Moines", 2743192))
		self.locationSet.add(CastingLocationObject("Kansas", 4098, "Colby", 2744027))
		self.locationSet.add(CastingLocationObject("Kansas", 4098, "Dodge City", 2743611))
		self.locationSet.add(CastingLocationObject("Kansas", 4098, "Hutchinson", 2743905))
		self.locationSet.add(CastingLocationObject("Kansas", 4098, "Topeka", 2743993))
		self.locationSet.add(CastingLocationObject("Kentucky", 4099, "Bowling Green", 2744510))
		self.locationSet.add(CastingLocationObject("Kentucky", 4099, "Lexington", 2744165))
		self.locationSet.add(CastingLocationObject("Louisiana", 4100, "Alexandria", 2744773))
		self.locationSet.add(CastingLocationObject("Louisiana", 4100, "Houma", 2744877))
		self.locationSet.add(CastingLocationObject("Louisiana", 4100, "Shreveport", 2744589))
		self.locationSet.add(CastingLocationObject("Maine", 4101, "Burlington", 2745226))
		self.locationSet.add(CastingLocationObject("Maine", 4101, "Presque Isle", 2744997))
		self.locationSet.add(CastingLocationObject("Maryland", 4102, "Glen Burnie", 2745487))
		self.locationSet.add(CastingLocationObject("Massachusetts", 4103, "Boston", 2746194))
		self.locationSet.add(CastingLocationObject("Michigan", 4104, "Detroit", 2746855))
		self.locationSet.add(CastingLocationObject("Michigan", 4104, "Grand Rapids", 2746529))
		self.locationSet.add(CastingLocationObject("Michigan", 4104, "Houghton", 2746440))
		self.locationSet.add(CastingLocationObject("Michigan", 4104, "Petoskey", 2746396))
		self.locationSet.add(CastingLocationObject("Minnesota", 4105, "Hibbing", 2747568))
		self.locationSet.add(CastingLocationObject("Minnesota", 4105, "Minneapolis", 2747175))
		self.locationSet.add(CastingLocationObject("Minnesota", 4105, "Roseau", 2747551))
		self.locationSet.add(CastingLocationObject("Mississippi", 4106, "Grenada", 2845439))
		self.locationSet.add(CastingLocationObject("Mississippi", 4106, "Mccomb", 2845146))
		self.locationSet.add(CastingLocationObject("Missouri", 4107, "Columbia", 2748153))
		self.locationSet.add(CastingLocationObject("Missouri", 4107, "Cape Girardeau", 2748195))
		self.locationSet.add(CastingLocationObject("Missouri", 4107, "Springfield", 2748376))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Anaconda", 2749125))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Glasgow", 2749329))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Great Falls", 2749102))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Havre", 2749168))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Kalispell", 2749139))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Laurel", 2749341))
		self.locationSet.add(CastingLocationObject("Montana", 4108, "Miles City", 2749119))
		self.locationSet.add(CastingLocationObject("Nebraska", 4109, "Chadron", 2749483))
		self.locationSet.add(CastingLocationObject("Nebraska", 4109, "Fremont", 2749506))
		self.locationSet.add(CastingLocationObject("Nebraska", 4109, "Lexington", 2749490))
		self.locationSet.add(CastingLocationObject("Nevada", 4110, "Battle Mountain", 2749925))
		self.locationSet.add(CastingLocationObject("Nevada", 4110, "Las Vegas", 2749893))
		self.locationSet.add(CastingLocationObject("Nevada", 4110, "Reno", 2749944))
		self.locationSet.add(CastingLocationObject("New Hampshire", 4111, "Berlin", 2750010))
		#self.locationSet.add(CastingLocationObject("New Jersey", 4112, "", x))
		self.locationSet.add(CastingLocationObject("New Mexico", 4113, "Albuquerque", 2750722))
		self.locationSet.add(CastingLocationObject("New Mexico", 4113, "Gallup", 2750809))
		self.locationSet.add(CastingLocationObject("New Mexico", 4113, "Roswell", 2750735))
		self.locationSet.add(CastingLocationObject("New Mexico", 4113, "Silver City", 2750784))
		self.locationSet.add(CastingLocationObject("New York", 4114, "Potsdam", 2751639))
		self.locationSet.add(CastingLocationObject("New York", 4114, "Rochester", 2751277))
		self.locationSet.add(CastingLocationObject("New York", 4114, "Utica", 2751461))
		self.locationSet.add(CastingLocationObject("North Carolina", 4115, "Hickory", 2752137))
		self.locationSet.add(CastingLocationObject("North Carolina", 4115, "Raleigh", 2752622))
		self.locationSet.add(CastingLocationObject("North Carolina", 4115, "Wilmington", 2752434))
		self.locationSet.add(CastingLocationObject("North Dakota", 4116, "Dickinson", 2752966))
		self.locationSet.add(CastingLocationObject("North Dakota", 4116, "Fargo", 2752735))
		self.locationSet.add(CastingLocationObject("North Dakota", 4116, "Rugby", 2752906))
		self.locationSet.add(CastingLocationObject("Ohio", 4117, "Lima", 2753056))
		self.locationSet.add(CastingLocationObject("Ohio", 4117, "Youngstown", 2753661))
		self.locationSet.add(CastingLocationObject("Oklahoma", 4118, "Enid", 2754290))
		self.locationSet.add(CastingLocationObject("Oklahoma", 4118, "Guymon", 2754719))
		self.locationSet.add(CastingLocationObject("Oklahoma", 4118, "Muskogee", 2754513))
		self.locationSet.add(CastingLocationObject("Oregon", 4119, "Bend", 2754838))
		self.locationSet.add(CastingLocationObject("Oregon", 4119, "Kiamath Falls", 2754903))
		self.locationSet.add(CastingLocationObject("Oregon", 4119, "Ontario", 2754946))
		self.locationSet.add(CastingLocationObject("Oregon", 4119, "Portland", 2754982))
		self.locationSet.add(CastingLocationObject("Oregon", 4119, "Roseburg", 2754855))
		self.locationSet.add(CastingLocationObject("Pennsylvania", 4120, "Allentown", 2755934))
		self.locationSet.add(CastingLocationObject("Pennsylvania", 4120, "Altoona", 2755323))
		#self.locationSet.add(CastingLocationObject("Puerto Rico", 8058, "", x))
		#self.locationSet.add(CastingLocationObject("Rhode Island", 4121, "", x))
		self.locationSet.add(CastingLocationObject("South Carolina", 4122, "Columbia", 2756812))
		self.locationSet.add(CastingLocationObject("South Dakota", 4123, "Aberdeen", 2756917))
		self.locationSet.add(CastingLocationObject("South Dakota", 4123, "Sioux Falls", 2757141))
		self.locationSet.add(CastingLocationObject("South Dakota", 4123, "Winner", 2757210))
		self.locationSet.add(CastingLocationObject("Tennessee", 4124, "Jackson", 2757474))
		self.locationSet.add(CastingLocationObject("Tennessee", 4124, "Knoxville", 2757437))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Conroe", 2758664))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Corpus Christi", 2758720))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Dallas", 2757960))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Kerrville", 2758519))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Killeen", 2757679))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Snyder", 2758855))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Hereford", 2757986))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Pecos", 2758794))
		self.locationSet.add(CastingLocationObject("Texas", 4125, "Wichita Falls", 2759066))
		self.locationSet.add(CastingLocationObject("Utah", 4126, "Blanding", 2759297))
		self.locationSet.add(CastingLocationObject("Utah", 4126, "Kanab", 2759247))
		self.locationSet.add(CastingLocationObject("Utah", 4126, "Salt Lake City", 2759288))
		#self.locationSet.add(CastingLocationObject("Vermont", 4132, "", x))
		self.locationSet.add(CastingLocationObject("Virgina", 4127, "Blacksburg", 2759663))
		self.locationSet.add(CastingLocationObject("Virgina", 4127, "Charlottesville", 2759501))
		self.locationSet.add(CastingLocationObject("Virgina", 4127, "Norfolk", 2759669))
		#self.locationSet.add(CastingLocationObject("Virgin Islands", 8059, "", x))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Kennewick", 2759815))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Seattle", 2759999))
		self.locationSet.add(CastingLocationObject("Washington", 4128, "Spokane", 2760234))
		#self.locationSet.add(CastingLocationObject("Washington DC", 8056, "", x))
		self.locationSet.add(CastingLocationObject("West Virgina", 4129, "Parkersburg", 2760601))
		self.locationSet.add(CastingLocationObject("Wisconsin", 4130, "Fond du Lac", 2760773))
		self.locationSet.add(CastingLocationObject("Wisconsin", 4130, "La Crosse", 2760873))
		self.locationSet.add(CastingLocationObject("Wisconsin", 4130, "Rhinelander", 2760972))
		self.locationSet.add(CastingLocationObject("Wyoming", 4131, "Casper", 2761351))
		self.locationSet.add(CastingLocationObject("Wyoming", 4131, "Gilette", 2761266))
		self.locationSet.add(CastingLocationObject("Wyoming", 4131, "Laramie", 2761250))
		self.locationSet.add(CastingLocationObject("Wyoming", 4131, "Rock Springs", 2761413))
		self.locationSet.add(CastingLocationObject("Wyoming", 4131, "Thermopolis", 2761314))

		return len(self.locationSet)