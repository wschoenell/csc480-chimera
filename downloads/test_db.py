#!/usr/bin/python
import sys
import MySQLdb
class database :
    conn = None
    cursor = None
    def __init__(self):
       try:
         self.conn = MySQLdb.connect(host = "localhost",user ="root",passwd="modha",db="test_db")
         self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
       except MySQLdb.Error,e:
           print "Error %d: %s" %(e.args[0],e.args[1])
           sys.exit(1)
     
    def InserToExposure_astromentry(self,G_RA,G_DEC,PATH):
         try:
            self.cursor.execute("INSERT INTO Exposure(Global_RA,Global_DEC,ImagePath,Time) VALUES (%s,%s)",(RA,DEC,PATH))

         except MySQLdb.Error, e:  
             print "Error %d: %s" % (e.args[0],e.args[1]) 
             sys.exit(1)

    def InsertToStar_scheduler(self,ObjectName,RA,DEC):
         try:
             self.cursor.execute("INSERT INTO Star(StarName,_RA,_DEC) VALUES (%s,%s,%s)",(ObjectName,RA,DEC))

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def InsertToStar_AM (self,RA,DEC,am):  
          try:
              self.cursor.execute("UPDATE Star SET _AM = %s WHERE _RA = %s AND _DEC = %s", (am,RA,DEC))  

          except MySQLdb.Error, e:
              print "Error %d: %s" % (e.args[0],e.args[1])
              sys.exit(1)

    def GetRaDecFlux(self,ID):
         try:
             self.cursor.execute("(SELECT * FROM(SELECT Star_id,_RA,_DEC,StarFlux FROM(Star,StarData) WHERE Star_id = Starid)as tmp WHERE Star_id = %s)",
             (ID))
             rows = self.cursor.fetchall()  
             print "RA        DEC        StarFlux" 
             for row in rows:
              print "%s, %s, %s" % (row["_RA"], row["_DEC"],row["StarFlux"])
             print "Number of rows returned: %d" % self.cursor.rowcount

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1]) 
             sys.exit(1)

    def CloseConnection(self):
           self.cursor.close()   
           self.conn.commit()
           self.conn.close()




test = database()
test.GetRaDecFlux("201010")
test.CloseConnection()
   
