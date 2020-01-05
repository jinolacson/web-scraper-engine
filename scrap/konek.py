import MySQLdb
from pprint import pprint

class Connection(object):
    
    	def __init__(self):
    	    
    	    self.db = None;
    	    self.cur = None;
    	    self.host = "localhost"
    	    self.user = "root"
    	    self.password = ""
    	    self.dbs = "fenix"
    	    self.cur = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.dbs) 
    	    self.lastids  = None
    	   
    	def cursors(self):
    	    
    	    return self.cur.cursor()
    	    
    	def close_connection(self):
    	    
    	    return self.cur.close();
    	
    	#insert query 
    	def insert(self,query):
    	    
    	    try:
    	        
    	        print "inserting parsed data.." , query
    	        
    	        curs = self.cursors()
    	        
    	        curs.execute(query)
    	        
    	        self.lastids = curs.lastrowid
    	        
                self.cur.commit()
    	        
    	    except Exception, e:
    	        
    	        print "error with" ,e
    	       
    	    #self.close_connection()
    	    
    	        
        #get the last inserted id	        
    	def lastid(self):
    	     
    	     return self.lastids
    	     
    	#view inserted values example table = descriptions     
    	def view(self,table):
    	    
    	    curs = self.cursors()
    	    
    	    curs.execute("SELECT * FROM "+table+" ")
    	    
    	    print "Table ", table , "values: "
    
            for row in curs.fetchall():
                
                pprint(row)
                
            self.close_connection()
            
            


try:
    q = Connection()
    
except Exception, e:
    
    print "Error initiating class connection" ,e
    

#q.insert(  """INSERT INTO descriptions (data) VALUES ('%s')""" % (items) )
#print q.lastid()


#q.view("descriptions")            

    	   
    