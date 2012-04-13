import httplib
import urllib
import urllib2
import cookielib

class MayhemCookiesHandler:
	def __init__(self, verbosity):
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.loginURL = "secure.modelmayhem.com"
		self.parameters = urllib.urlencode({"email": "gbudiman@purdue.edu",
							"password": "80ae11f0",
							"reme": "1",
							"check": "login"})
		self.headers = {"Content-type": "application/x-www-form-urlencoded",
					"Accept": "text/plain"}
					
		response = self.testAwake(verbosity)
		if (response.status != 302):
			print "Terminating run"
			return -1
		
		response = self.sendLoginRequest(verbosity)
		
		
		r = self.opener.open("http://modelmayhem.com/casting/search_casting")
		print r.read()
		
	def testAwake(self, verbosity):
		loginPage = httplib.HTTPConnection(self.loginURL)
		loginPage.request("GET", "/login")
		response = loginPage.getresponse()
		if verbosity == 1:
			print "Login page request returns", response.status, response.reason
		
		return response
		
	def sendLoginRequest(self, verbosity):
		#request = urllib2.Request("".join([self.loginURL, "/login/action"]), self.parameters, self.headers)
		#response = urllib2.urlopen("".join(["https://", self.loginURL]), self.parameters)
		self.opener.open('https://secure.modelmayhem.com/login/action', self.parameters)
		#self.cj.extract_cookies(response, request)