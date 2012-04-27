# -*- coding: utf-8 -*-
import re
import sys
import string
from MayhemCastingParser import MayhemCastingParser
from BrowseDataObject import BrowseDataObject

class MayhemBrowseParser(MayhemCastingParser):
	def __init__(self, verbosity):
		super(MayhemBrowseParser, self).__init__(verbosity)
		
	def parse(self, dataDict, result):
		profession = re.findall("[\"][>]([A-Z a-z/]*)</div>[\n\r\t]+(?:</td>)", result)
		ID = re.findall("(?:<a href=\"/)([0-9]+)(?:\" target)", result)
		location = re.findall("([\w ]+)[,][ ]([\w ]+)[,][ ]([A-Z \'\-a-z]+)[\t]+(?:</td>)", result)
		gender = re.findall("(?:Gender:</td>)[\n\r\t]+(?:<td class=\"data1\">)(Female|Male|n/a)(?:</td>)", result)
		lastActivity = re.findall("([A-Za-z.]+)[ ]([0-9]{1,2})[,][ ]([0-9]{4})", result)
		compensation = re.findall("(?:Compensation:</td>)[\n\r\t]+(?:<td>)([A-Z/ a-z]+)(?:</td>)", result)
		experience = re.findall("(?:Experience:</td>)[\n\r\t]+(?:<td>)([A-Z/ a-z]+)(?:</td>)", result)
		shootNudes = re.findall("(?:Shoot Nudes:</td>)[\n\r\t]+(?:<td>)(?:(yes|no|n/a))(?:</td>)", result)
		
		iProfession = iter(profession)
		iLocation = iter(location)
		iGender = iter(gender)
		iLastActivity = iter(lastActivity)
		iShootNudes = iter(shootNudes)
		iCompensation = iter(compensation)
		iExperience = iter(experience)
		browseCount = 0
		
		if len(ID) == len(profession)\
			and len(ID) == len(location)\
			and len(ID) == len(gender)\
			and len(ID) == len(location)\
			and len(ID) == len(lastActivity)\
			and len(ID) == len(compensation)\
			and len(ID) == len(experience):
			for iID in ID:
				cProfession = iProfession.next()
				dataDict[int(iID)] = BrowseDataObject(cProfession\
													, iLocation.next()\
													, iGender.next()\
													, iLastActivity.next()\
													, iShootNudes.next() if cProfession == 'Model' else None\
													, iCompensation.next()\
													, iExperience.next())
				browseCount += 1
				
			if self.verbosity == 1:
				print ">>>", browseCount, "returned"
			return browseCount
		else:
			if self.verbosity == 1:
				print "Mismatched regex results", len(ID)
				print "Profession", len(profession)
				print "Gender", len(gender)
				print "Location", len(location)
				print "Last Activity", len(lastActivity)
				print "Compensation", len(compensation)
				print "Experience", len(experience)
				for d in profession:
					print d, iLocation.next(), iGender.next(), iLastActivity.next()
					if d == 'Model':
						print ' -- shoot nudes?', iShootNudes.next()
					print ' --', iCompensation.next(), iExperience.next()
			return - 1