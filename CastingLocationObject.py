# -*- coding: utf-8 -*-
class CastingLocationObject:
	def __init__(self, country, state, stateID):
		self.country = country
		self.state = state
		self.stateID = stateID
		
	def read(self):
		return self.country + "." + self.state 
		
	def getCountry(self):
		return self.country

	def getState(self):
		return self.stateID
		
