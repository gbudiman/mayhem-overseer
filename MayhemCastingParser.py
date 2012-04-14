# -*- coding: utf-8 -*-
import re
import sys

class MayhemCastingParser:
	def __init__(self, verbosity):
		self.existingCasting = []
		self.verbosity = verbosity
		
	def parse(self, result):
		print "Parsing", sys.getsizeof(result) / 1024, "KB"