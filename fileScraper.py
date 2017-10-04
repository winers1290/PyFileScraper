#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import requests
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

class fileScraper:

	def __init__(self):

		#Parse URL
		self.url = self.parseURL(sys.argv[1])
		self.parsedurl = urlparse(self.url)
		#Declare variables
		self.fileExtensions = ['.asc', '.txt', '.tar.gz', '.gz', '.tar', '.py', '.zip', '.rar', '.pdf', '.doc', '.dot', '.docx', '.docm', '.dotx', '.docm', '.docb', '.xls', '.xlt', '.xlm', '.xlsx', '.xlsm', '.xlxt', '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.csv', '.json', '.xml', '.ppt', '.pptx', '.pptm', '.potx', '.potm', '.ppam', '.ppsm', '.sldx', '.sldm', '.pub', '.xps', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.tiff', '.bmp', '.stl']
		self.pageArray = [self.prettyUrl(self.parsedurl)] #List of all page links
		self.scrapedPages = [] #List of pages successfully scraped
		self.files = []
		self.parsedUrl = ''
		self.loopCount = 0
		self.loop =  True

		return

	def prettyUrl(self, url):
		#Check for GET
		if url.query != "":
			return self.scheme + '://{uri.netloc}{uri.path}?{uri.query}/'.format(uri=url).rstrip('/')
		else:
			return self.scheme + '://{uri.netloc}{uri.path}/'.format(uri=url).rstrip('/')



	def parseURL(self, url):
		self.parsedUrl = urlparse(url)
		self.scheme = '{uri.scheme}'.format(uri=self.parsedUrl)
		self.domain = '{uri.netloc}'.format(uri=self.parsedUrl)
		return url

	def parseResult(self, link):
		href = link['href']

		#Parse URL
		url = urlparse(href)
		url_domain = '{uri.netloc}'.format(uri=url)

		#Check link does not have a file extensions
		for ext in self.fileExtensions:
			#Check URL path, not the href. This filters out GET queries
			#which can be common nowadays to dynamically resize images.
			if len(url.path) > len(ext) and url.path[(len(ext) * -1):] == ext:
				return

		#Check link is on the same domain
		if self.domain == url_domain and '@' not in url.geturl() and 'share=' not in url.geturl():
			#Domain is the same. Iterate over paths to check for duplicate
			if self.prettyUrl(url) not in self.pageArray:
				#Make sure URL is constructed properly, and store
				self.pageArray.append(self.prettyUrl(url))

		#Filter our relative links
		elif url_domain == "": #Indicates relative or special link
			#remove all the special types of link
			if url.scheme == "mailto" or url.scheme == "tel" or url.scheme == "javascript" or '@' in url.geturl() or 'share=' in url.geturl():
				pass
			else:
				#Now remove pseudo #links
				if isinstance(href, str) and len(href) > 1:
					if href[0] == "#":
						pass
					else:
						#Link is relative, make absolute
						url = urljoin(self.url, url.path)
						url = urlparse(url)
						if self.prettyUrl(url) not in self.pageArray:
							self.pageArray.append(self.prettyUrl(url))


		return

	def findFiles(self, link):

		try:
			href = link['href']
			url = urlparse(link['href'])
		except KeyError:
			try:
				href = link['src']
				url = urlparse(link['src'])
			except KeyError:
				return False


		#Check for cool file extensions
		for ext in self.fileExtensions:
			if len(url.path) > len(ext) and url.path[(len(ext) * -1):] == ext:
				#We have a match
				if url.scheme == "":
					#Construct absolute URL and check for duplicates
					joinedurl = urljoin(self.prettyUrl(self.parsedurl), url.path)
					url = urlparse(joinedurl)

				if self.prettyUrl(url) not in self.files:
					self.files.append(self.prettyUrl(url))

	def head(self, url):
		try:
			head = requests.head(url)
			return head
		except Exception as e: #There are lots of reasons why this could fail
			return False

	def get(self, url):
		try:
			r = requests.get(url)
			return r
		except Exception as e: #There are lots of reasons why this could fail
			return False

	def makeRequest(self, url):

		head = self.head(url)
		if head is not False and head.status_code == 200: #Check HEAD first (lightweight)
			get = self.get(url)
			if get is False or get.status_code != 200:
				self.loopCount = self.loopCount + 1
				return False

		else: #If HEAD fails (possibly due to rejecting this protocol, check GET)
			get = self.get(url)
			if get is False or get.status_code != 200:
				self.loopCount = self.loopCount + 1
				return False

		#If we get to here, GET has returned 200 code
		if hasattr(get, 'text'):
			if isinstance(get.text, str) and len(get.text) > 0:
				return get.text
			else:
				self.loopCount = self.loopCount + 1
				return False
		else:
			self.loopCount = self.loopCount + 1
			return False

	def scrapeLoop(self):
		while True:

			try:
				url = self.pageArray[self.loopCount]
			except IndexError:
				break

			print("Searching: " + url)

			result = self.makeRequest(url)
			if result is not False:

				soup = BeautifulSoup(result, "html.parser")

				#Find Links
				for link in soup.find_all('a', href=True):
					self.parseResult(link)

				#Find files
				for link in soup.find_all(['a', 'img', 'video', 'input', 'meta']):
					self.findFiles(link)

			self.loopCount = self.loopCount + 1

		self.windUp()
		return

	def windUp(self):
		if len(self.files) > 0:
			print("---- FOUND " + str(len(self.files)) + " FILES ----")
			for file in self.files:
				print(file)



#Load
fs = fileScraper()

#Scrape
fs.scrapeLoop()
