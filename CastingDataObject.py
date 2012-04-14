# -*- coding: utf-8 -*-
class CastingDataObject:
	def __init__(self, profession, seeking, city, nudity, compensation):
		self.profession = profession
		self.seeking = seeking
		self.city = city
		self.nudity = nudity
		self.compensation = compensation
		
	def dump(self):
		return self.profession, "seeking", self.seeking, "@", self.city\
			, self.nudity, self.compensation