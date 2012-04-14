# -*- coding: utf-8 -*-
class CastingLocationObject:
	def __init__(self, state, stateID, town, townID):
		self.state = state
		self.stateID = stateID
		self.town = town
		self.townID = townID
		
	def read(self):
		return self.state + "." + self.town
		
	def getState(self):
		return self.stateID
		
	def getTown(self):
		return self.townID