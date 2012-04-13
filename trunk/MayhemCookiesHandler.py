import httplib
import urllib

class MayhemCookiesHandler:
	def __init__(self, verbosity):
		self.loginURL = "secure.modelmayhem.com"
		self.parameters = urllib.urlencode({"@email": "gbudiman@purdue.edu",
							"@password": "80ae11f0",
							"@reme": "1",
							"@check": "login"})
		self.headers = {"Content-type": "application/x-www-form-urlencoded",
					"Accept": "text/plain"}
					
		response = self.testAwake(verbosity)
		if (response.status != 302):
			print "Terminating run"
			return -1
		
		response = self.sendLoginRequest(verbosity)
		if (response.status != 302):
			print "Terminating run"
			return -1
		
		print response.getheaders()
		#for setpiece in response.getheaders():
		#	print setpiece
		
	def testAwake(self, verbosity):
		loginPage = httplib.HTTPConnection(self.loginURL)
		loginPage.request("GET", "/login")
		response = loginPage.getresponse()
		if verbosity == 1:
			print "Login page request returns", response.status, response.reason
		
		return response
		
	def sendLoginRequest(self, verbosity):
		execLogin = httplib.HTTPConnection(self.loginURL)
		execLogin.request("POST", "/login/action", self.parameters, self.headers)
		response = execLogin.getresponse()
		if verbosity == 1:
			print "Login POST request returns", response.status, response.reason
			
		return response