# -*- coding: utf-8 -*-
from datetime import date
class BrowseDataObject:
	def __init__(self, profession, location, gender, lastActivity, shootNudes, compensation, experience):
		monthDict = {'Jan.': 1
					, 'Feb.': 2
					, 'Mar.': 3
					, 'Apr.': 4
					, 'May.': 5
					, 'Jun.': 6
					, 'Jul.': 7
					, 'Aug.': 8
					, 'Sep.': 9
					, 'Oct.': 10
					, 'Nov.': 11
					, 'Dec.': 12}
		compensationDict = {'Any': 0
						  , 'Depends on Assignment': 1
						  , 'Paid Assignments Only': 2
						  , 'Time for Print': 3
						  , 'n/a': 4}
		experienceDict = {'No Experience': 0
						, 'Some Experience': 1
						, 'Experienced': 2
						, 'Very Experienced': 3
						, 'n/a': 4}
		self.profession = profession
		hotspot = location.strip().split(',')
		self.country = hotspot[2].strip()
		self.state = hotspot[1].strip()
		self.town = hotspot[0].strip()
		if gender == 'Male':
			self.gender = 0
		elif gender == 'Female':
			self.gender = 1
		else:
			self.gender = 2 # Gender can be undefined
		self.lastActivity = date(int(lastActivity[2]), monthDict[lastActivity[0]], int(lastActivity[1]))
		if shootNudes == 'yes':
			self.shootNudes = 1
		elif shootNudes == 'no':
			self.shootNudes = 0
		else:
			self.shootNudes = None
		#print experience, compensationDict[experience.strip()]
		self.compensation = compensationDict[compensation]
		self.experience = experienceDict[experience]