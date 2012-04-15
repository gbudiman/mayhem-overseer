# -*- coding: utf-8 -*-
import re
import sys
import string
from CastingDataObject import CastingDataObject

class MayhemCastingParser:
	def __init__(self, verbosity):
		self.existingCasting = []
		self.verbosity = verbosity
		
	def parse(self, dataDict, result):
		profession = re.findall("[\"][>]([A-Z a-z/]*)</div>.*[\n\r\t]+.*(?:ccViewDetails)", result)
		ID = re.findall("\"#\"><a href=\"/casting/([0-9]+)[?]", result)
		seeking = re.findall("[\n\r\t]+((Female Models)<br>|(Male Models)<br>|(Photographer)<br>|\
(Makeup Artist)<br>|(Hair Stylist)<br>|(Wardrobe Stylist)<br>|\
(Retoucher)<br>|(Artist/Painter)<br>|(Body Painter)<br>|\
(Publication)<br>|(Filmmaker)<br>|(Clothing Designer)<br>|\
(Approved Agency)<br>|(Digital Artist)<br>)+[\n\r\t]+</td>", result)
		location = re.findall("<td colspan=\"3\">[\n\r\t]*([A-Z, \'\-a-z]+)<br />", result)
		nudity = re.findall("Nudity:</b><br/>[\n\r\t]*(Yes|No)", result)
		compensation = re.findall("<td>(Paid|TFMMVIP|Negotiable|TF|Unpaid Test)", result)
		
		#for d in profession:
		#	print d
		#print ID
		#for d in location:
		#	print d
		#for d in nudity:
		#	print d
		#for d in seeking:
		#	print tuple(set(d[1:]))[1:]
		#for d in compensation:
		#	print d
		
		iProfession = iter(profession)
		iNudity = iter(nudity)
		iCompensation = iter(compensation)
		iLocation = iter(location)
		iSeeking = iter(seeking)
		castingCount = 0
		if len(ID) == len(profession)\
			and len(ID) == len(nudity)\
			and len(ID) == len(compensation)\
			and len(ID) == len(location)\
			and len(ID) == len(seeking):	
			for iID in ID:
				# skip key check, doesn't really matter anyway
				dataDict[int(iID)] = CastingDataObject(iProfession.next(), tuple(set(iSeeking.next()[1:]))[1:]\
												, iLocation.next(), iNudity.next(), iCompensation.next())
				castingCount += 1
				
			if self.verbosity == 1:
				print ">>>", castingCount, "returned"
			return castingCount	
				
		else:
			if self.verbosity == 1:
				print "Mismatched regex results", len(ID)
				print "Profession", len(profession)
				print "Nudity", len(nudity)
				print "Compensation", len(compensation)
				print "Location", len(location)
				print "Seeking", len(seeking)
			return -1
