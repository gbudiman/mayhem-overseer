# -*- coding: utf-8 -*-
class CastingDataObject:
	def __init__(self, profession, seeking, town, state, country, nudity, compensation):
		self.profession = profession
		self.seeking = seeking
		self.town = town
		self.state = state
		self.country = country
		self.nudity = nudity
		self.compensation = compensation
		
	def dump(self):
		return self.profession, "seeking", self.seeking, "@", self.town\
			, self.state, self.nudity, self.compensation
			
