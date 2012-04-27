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
		location = re.findall("([A-Z \'\-a-z]+)[,][ ]([A-Z \'\-a-z]+)[,][ ]([A-Z \'\-a-z]+)[\t]+(?:</td>)", result)
		gender = re.findall("(?:data1\">)([FeMmalen/]+)", result)
		lastActivity = re.findall("([A-Za-z.]+)[ ]([0-9]{1,2})[,][ ]([0-9]{4})", result)
		compensation = re.findall("(?:Compensation:</td>)[\n\r\t]+(?:<td>)([A-Z/ a-z]+)(?:</td>)", result)
		experience = re.findall("(?:Experience:</td>)[\n\r\t]+(?:<td>)([A-Z/ a-z]+)(?:</td>)", result)
		shootNudes = re.findall("(?:Shoot Nudes:</td>)[\n\r\t]+(?:<td>)(?:(yes|no))(?:</td>)", result)
		
		iProfession = iter(profession)
		iLocation = iter(location)
		iGender = iter(gender)
		iLastActivity = iter(lastActivity)
		iShootNudes = iter(shootNudes)
		iCompensation = iter(compensation)
		iExperience = iter(experience)
		browseCount = 0
		
		#for d in profession:
		#	print d, iLocation.next(), iGender.next(), iLastActivity.next()
		#	if d == 'Model':
		#		print ' -- shoot nudes?', iShootNudes.next()
		#	print ' --', iCompensation.next(), iExperience.next()