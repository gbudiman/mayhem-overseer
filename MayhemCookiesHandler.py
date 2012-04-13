# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2
import cookielib
import re

class MayhemCookiesHandler:
	def __init__(self, verbosity):
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		self.loginURL = "secure.modelmayhem.com"
		self.loginLaunchURL = "https://secure.modelmayhem.com/login/action"
		self.castingURL = "http://modelmayhem.com/casting/search_casting"
		self.loginConfirmation = "Welcome, Gloria Budiman!"
		self.parameters = urllib.urlencode({"email": "gbudiman@purdue.edu",
							"password": "80ae11f0",
							"reme": "1",
							"check": "login"})
		self.headers = {"Content-type": "application/x-www-form-urlencoded",
					"Accept": "text/plain"}
		self.execute(verbosity)
					
	def execute(self, verbosity):
		response = self.testAwake(verbosity)
		if (response.status != 302):
			print "Terminating run"
			return -1
		
		successfulLogin = self.sendLoginRequest(verbosity)
		if (successfulLogin == None):
			print "Login failed. Terminating run"
			return -2
		
	def testAwake(self, verbosity):
		loginPage = httplib.HTTPConnection(self.loginURL)
		loginPage.request("GET", "/login")
		response = loginPage.getresponse()
		if verbosity == 1:
			print "Login page request returns", response.status, response.reason
		
		return response
		
	def sendLoginRequest(self, verbosity):
		self.opener.open(self.loginLaunchURL, self.parameters)
		castingPage = self.opener.open(self.castingURL)
		return re.search(self.loginConfirmation, castingPage.read())
		