class Link:
	def __init__(self,tr):
		self.tr = tr	
		self.linkid = tr['id']
		imgs = tr.find_all('img')
		
		self.formatImg = None

		self.favicon = None
		
		self.source = None

		if len(imgs) > 0:
			self.favicon = imgs[0].get('src')
			a = imgs[0].parent.find_all('a')
			self.source = a[0].get_text().strip()
			
		if len(imgs) > 1: 					
			self.formatImg = imgs[1]['src']
		
		self.age = None
		tds = tr.find_all('td')

		ageList = []
		
		for td in tds:
			cLass = td.get('class')
			if cLass is None: continue
			if 'ageCell' in cLass:
				ageList.append(td.get_text().strip())
		
		#the age in str
		if len(ageList) > 0:
			self.age = ageList[0]
		
		#the votes list
		self.votes = []
		votesList = []
		
		for td in tds:
			cLass = td.get('class')
			if cLass is None: continue
			if 'votesCell' in cLass:
				votesList.append(td.get_text().replace("\n","").strip().split(" "))
				
		for vote in votesList:
			for v in vote:
				if v.strip() !='':
					self.votes.append(v)
					
		#the quality (HD, cam ..etc)
		self.quality = None
		qualityList = []
		
		for td in tds:
			cLass = td.get('class')
			if cLass is None: continue
			if 'qualityCell' in cLass:
				qualityList.append(td.get_text().strip())
		
		self.quality = qualityList[0]
		
	#links
	def getlink(self):
		return 'http://cinema.solarmovie.ph/link/play/%s/' % self.linkid.split('_')[1]
	#age	
	def getage(self):
		return self.age
		
	#quality hd, cam		
	def getquality(self):
		return self.quality
	
	#link favicon	
	def getfavicon(self):
		return self.favicon
		
	#favicon src	
	def getfaviconsrc(self):
		return self.source 
		
	#votes likes	
	def getvotes(self):
		return self.votes[0]
		
	#votes likes video	
	def getvotesvideo(self):
		return self.votes[1]
	
	#votes likes audio	
	def getvotesaudio(self):
		return self.votes[2]
			