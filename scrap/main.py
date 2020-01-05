movie = "https://www.solarmovie.ph/advanced-search/?q%5Btitle%5D=&q%5Bis_series%5D=1&q%5Blinks%5D=1&q%5Bactor%5D=&q%5Bdirector%5D=&q%5Bdescription%5D=&q%5Byear_from%5D=1893&q%5Byear_to%5D=2016&q%5Bimdb_rating_from%5D=0&q%5Bimdb_rating_to%5D=0&q%5Bsolar_rating_from%5D=0&q%5Bsolar_rating_to%5D=0&q%5Bcountry%5D=0&q%5Blanguage%5D=0"

from solar import *
from description import Description
from con import *

lks = {}

def donelink(page):
	#print "threads:",SolarPage.threads,"Done link",page.link.getlink()
	print page.link.getlink()
	

def donedescriptions(desc,title,year):
	print "threads:",SolarPage.threads,"Done link", desc, " " , title , " ", year
	
def donedetail(mv):
	
	donedescriptions(mv.getdescriptions(),mv.gettitle(),mv.getyear())
	
	for link in mv.getlinks():
		page = SolarPlayPage.getpage(link)
		page.ondone(donelink)
		page.start()
		
def donelist(ls):
	for mv in ls.getmovies():
		mv.ondone(donedetail)
		mv.start()

def loopurlmovie():
	for i in range(0, 1656):#maximum pagination number
		yield "https://www.solarmovie.ph/advanced-search/?q%5Btitle%5D=&q%5Bis_series%5D=1&q%5Blinks%5D=1&q%5Bactor%5D=&q%5Bdirector%5D=&q%5Bdescription%5D=&q%5Byear_from%5D=1893&q%5Byear_to%5D=2016&q%5Bimdb_rating_from%5D=0&q%5Bimdb_rating_to%5D=0&q%5Bsolar_rating_from%5D=0&q%5Bsolar_rating_to%5D=0&q%5Bcountry%5D=0&q%5Blanguage%5D=0&page={0}".format(i) 
	
if __name__ == '__main__':
	
	'''
	for i in loopurlmovie():
		s = SolarListPage(i)
		s.ondone(donelist)
		s.start()
	'''		
	
	s = SolarListPage(movie)
	s.ondone(donelist)
	s.start()
	
	
	while True:
		time.sleep(1)
		
		dead = 0
		for th in SolarPage.threads:
			if th.done:
				dead = dead + 1
		
		if len(SolarPage.threads) == dead:
			break
		
		#print dead, len(SolarPage.threads)
	