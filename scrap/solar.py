import urllib2,urllib, time, threading
from bs4 import BeautifulSoup
from link import Link

class SolarPage(threading.Thread):
	threads = []
	def __init__(self,url):
		self.done = False
		self.url = url
		self.pageloaded = False
		self.souploaded = False		
		self.error = False
		self.donefunc = None
		threading.Thread.__init__(self)
	
	def run(self):
		try:
			SolarPage.threads.append(self)
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')]
			pagestr = None
			print 'Getting',self.url
			try:
				pagestr = opener.open(self.url).read()	
			except:
				print "Error with",self.url
				self.error = True
				return
			print 'Loading soup',self.url
			
			self.pageloaded = True
			self.soup = BeautifulSoup(pagestr,'lxml')
			self.souploaded = True
			print 'Calling ondone',self.url
			if self.donefunc is not None: self.donefunc(self)

		except Exception,e:
			print e
		
		self.done = True
		
	def waitpage(self):
		while True:
			if self.pageloaded or self.error:
				break
			time.sleep(0.1)	
				
	def waitsoup(self):
		while True:
			if self.souploaded or self.error:
				break
			time.sleep(0.2)	
	def wait(self):
		self.waitpage()
		self.waitsoup()
	
	def ondone(self,func):
		self.donefunc = func
		
class SolarListPage(SolarPage):
		
	def getmovies(self):
		for a in self.soup.find_all('a'):
			cLass = a.get('class')
			if cLass is None: continue
			if 'coverImage' in cLass:
				title = a.get('title')
				year = title.split('(')[-1]
				year = year[:-1]
				title = title.replace("("+year+")","")
				
				yield SolarDetailPage('https://www.solarmovie.ph%s' % a.get('href') ,title,year)
				break #for testing, 1 movie only
		
	def getmovielinks(self):
		for a in self.soup.find_all('a'):
			cLass = a.get('class')
			if cLass is None: continue
			if 'coverImage' in cLass:
				title = a.get('title')
				year = title.split('(')[-1]
				year = year[:-1]
				title = title.replace("("+year+")","")
				
				yield 'https://www.solarmovie.ph%s' % a.get('href')
				

class SolarDetailPage(SolarPage):
	def __init__(self,url,title,year):
		
		SolarPage.__init__(self,url)
		
		self.title = title
		self.year = year
		
	def getlinks(self):
		for tr in self.soup.find_all('tr'):
			cLass = tr.get('class')
			if cLass is None: continue
			if u'odd' in cLass or u'even' in cLass:	
				yield Link(tr)
				
	#movie title			
	def gettitle(self):
		return self.title
	
	#movie year	
	def getyear(self):
		return self.year
	
	#movie descriptions	
	def getdescriptions(self):
		for d in self.soup.find_all('p'):
			cLasss = d.get('class')
			if cLasss is None: continue
			if 'description' in cLasss:
				return d.getText()
		

		
class SolarPlayPage(SolarPage):
	
	@staticmethod
	def getpage(link):
		return SolarPlayPage(link)
	def __init__(self,link):
		url = link.getlink()
		SolarPage.__init__(self,url)
		
		self.link = link	

	def getiframelink(self):
		iframes = self.soup.find_all('iframe')
		if len(iframes) > 0:
			return iframes[0].get('src')

