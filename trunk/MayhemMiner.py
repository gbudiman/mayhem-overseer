from MayhemCookiesHandler import MayhemCookiesHandler

class MayhemMiner:
	def __init__(self, verbosity):
		self.mine(verbosity)
		
	def mine(self, verbosity):
		cookies = MayhemCookiesHandler(verbosity)