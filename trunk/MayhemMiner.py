# -*- coding: utf-8 -*-
from MayhemCookiesHandler import MayhemCookiesHandler
from MayhemRequestHandler import MayhemRequestHandler

class MayhemMiner:
	def __init__(self, verbosity):
		self.mine(verbosity)
		
	def mine(self, verbosity):
		page = MayhemCookiesHandler(verbosity)
		
		if page == -1:
			return -1
		elif page == -2:
			return -2
		else:
			request = MayhemRequestHandler("http://www.modelmayhem.com/casting/result/?", page)
			request.launchRequest(1)
			
		return 0