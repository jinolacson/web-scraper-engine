#!/usr/bin/env python
import threading
import time
from bs4 import BeautifulSoup
import urllib2
import logging

ls = []
class movies (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.url1 = "https://www.solarmovie.ph/advanced-search/?q%5Btitle%5D=&q%5Bis_series%5D=1&q%5Blinks%5D=1&q%5Bactor%5D=&q%5Bdirector%5D=&q%5Bdescription%5D=&q%5Byear_from%5D=1893&q%5Byear_to%5D=2016&q%5Bimdb_rating_from%5D=0&q%5Bimdb_rating_to%5D=0&q%5Bsolar_rating_from%5D=0&q%5Bsolar_rating_to%5D=0&q%5Bcountry%5D=0&q%5Blanguage%5D=0"     
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        threadLock.acquire()
        print_time(self.name, self.counter, True, self.url1)
        # Free lock to release next thread
        threadLock.release()

def print_time(threadName, delay, counter, url1):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        try:
            soup = BeautifulSoup(urllib2.urlopen(url1).read())
        except Exception, e:
            print "error with", url1
        for a in soup.find_all('a'):
            cLass = a.get('class')
            if cLass is None: continue
            if 'coverImage' in cLass:
                title = a.get('title')
                year = title.split('(')[-1]
                year = year[:-1]
                title = title.replace("("+year+")","")
                
                crawlinks('https://www.solarmovie.ph%s' % a.get('href'))
        counter = False

def crawlinks(list):
        try:
            soup = BeautifulSoup(urllib2.urlopen(list).read())
        except Exception, e:
            print "error with", list

        #description
        #for a in soup.find_all('p'):
            #cLass = a.get('class')
            #if cLass is None: continue
            #if 'description' in cLass:
                #print a.getText()

        #poster image, genres,country,language
        #for a in soup.find_all('div'):
        #    cLass = a.get('class')
        #    if cLass is None: continue
        #    if 'overViewBox' in cLass:
        #        overView = a.string
                #print a.getText()#dae pa naaali ang semicolon genres,country,language
                #print soup.findAll('img')[0].get('src')

        #iframe informations
        for tr in soup.find_all('tr'):
            cLass = tr.get('class')
            if cLass is None : continue
            if 'sponsorLink' in cLass : continue
            if 'hidden' in cLass : continue
            if 'nohover' in cLass : continue
            else:
                #video links
                linkid = 'http://cinema.solarmovie.ph/link/play/%s/' % tr['id'].split('_')[1]
                imgs = tr.find_all('img')

                #favicon src image and text
                if len(imgs) > 0:
                    srcs = imgs[0].get('src')
                    a = imgs[0].parent.find_all('a')
                    texts = a[0].get_text().strip()
                
                #format image flash
                if len(imgs) > 1:                   
                    formatImg = imgs[1]['src']

                age = None
                tds = tr.find_all('td')

                ageList = []
                
                for td in tds:
                    cLass = td.get('class')
                    if cLass is None: continue
                    if 'ageCell' in cLass:
                        ageList.append(td.get_text().strip())
                
                #the age in str
                if len(ageList) > 0:
                    ageList[0]

                votes = []
                votesList = []
                
                for td in tds:
                    cLass = td.get('class')
                    if cLass is None: continue
                    if 'votesCell' in cLass:
                        votesList.append(td.get_text().replace("\n","").strip().split(" "))

                #for vote in votesList:
                #    for v in vote:
                #        if v.strip() !='':
                #            print v

                quality = None
                qualityList = []
                
                for td in tds:
                    cLass = td.get('class')
                    if cLass is None: continue
                    if 'qualityCell' in cLass:
                        qualityList.append(td.get_text().strip())
                
                        print qualityList[0]


                            
                        
                        
                        
                    #if 'votesCell' in cLasstd : 
                    #if 'qualityCell' in cLasstd : 
                    #if 'ageCell' in cLasstd : 
                    




                
                #print a.find('img')
                #for lnks in a.find_all('a', href=True):
                #    print a
                    #print "https://www.solarmovie.ph%s" % lnks["href"]            #if 'votesCell' in cLass:
            #    print a.get("span")

                

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = movies(1, "movies", 1)
#thread2 = tvshows(2, "tvshows", 2)

# Start new Threads
thread1.start()
#thread2.start()

# Add threads to thread list
threads.append(thread1)
#threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"