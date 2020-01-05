#!/usr/bin/env python
import threading
from pprint import pprint
#import logging

#logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class MyThread(threading.Thread):

    def __init__(self,count):
        self.done = False
        self.donefunc = None
        self.count = count
        threading.Thread.__init__(self)

    def run(self):

        try:
            try:
                print "calling:" , self.count
                
            except Exception, e:
                print "error:" , self.count

            print 'ondone:',self.count
            if self.donefunc is not None: self.donefunc(self)
           
                

        except Exception, e:
            print e

        self.done = True


    def ondone(self,func):
        self.donefunc = func


def done(ls):
    print "" , ls
         
       

for i in range(10):
    t = MyThread(i)
    t.ondone(done)
    t.start()