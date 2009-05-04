#!/usr/bin/python
import sys
import MySQLdb
class database :
    conn = None
    cursor = None
    def __init__(self):
       try:
         self.conn = MySQLdb.connect(host = "localhost",user ="modha",passwd="802528907",db="chimera")
         self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
       except MySQLdb.Error,e:
           print "Error %d: %s" %(e.args[0],e.args[1])
           sys.exit(1)
     
    def add_Exposure(self,path,G_RA,G_DEC):
         try:
            self.cursor.execute("SELECT add_Exposure(%s,%s,%s)",(path,G_RA,G_DEC))
            row = self.cursor.fetchone()
            return row.values()[0]
            
         except MySQLdb.Error, e:  
             print "Error %d: %s" % (e.args[0],e.args[1]) 
             sys.exit(1)

    def add_Star(self,_RA,_DEC,flux,seeing,magnitude,exposureid):
         try:
            self.cursor.execute("SELECT Insert_Star(%s,%s,%s,%s,%s,%s)",(_RA,_DEC,flux,seeing,magnitude,exposureid))
            row = self.cursor.fetchone()
            starcount = row.values()[0]
            return starcount

         except MySQLdb.Error, e:  
             print "Error %d: %s" % (e.args[0],e.args[1]) 
             sys.exit(1) 


    def get_Flux(self,StarID):
         try:
            self.cursor.execute("SELECT getFlux(%s)",(StarID))
            row = self.cursor.fetchone()
            return row.values()[0] 
            

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def get_FWHM(self,ID):
         try:
            self.cursor.execute("SELECT getFWHM(%s)",(ID))
            row = self.cursor.fetchone()
            seeing = row.values()[0] 
            return seeing 

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def get_Magnitude(self,ID):
         try:
            self.cursor.execute("SELECT getMAG(%s)",(ID))
            row = self.cursor.fetchone()
            magnitude = row.values()[0] 
            return magnitude

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def get_AirMass(self,ID):
         try:
            self.cursor.execute("SELECT getAM(%s)",(ID))
            row = self.cursor.fetchone()
            airmass = row.values()[0] 
            return airmass 

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)
    

    def get_ExposureID(self,ImagePath):
         try:
            self.cursor.execute("SELECT getExposureID(%s)",(ImagePath))
            row = self.cursor.fetchone()
            exposureid = row.values()[0] 
            return exposureid

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)
    
    def get_ImagePath(self,ExposureID):
         try:
            self.cursor.execute("SELECT getImagePath(%s)",(ExposureID))
            row = self.cursor.fetchone()
            imagepath = row.values()[0] 
            return imagepath

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def get_StarID(self,_ra,_dec):
	 try:
	    self.cursor.execute("SELECT Star_id FROM Star WHERE _RA = %s AND _DEC =%s ORDER BY Star_id ASC",(_ra,_dec))
            rows = self.cursor.fetchall()
            starid = []
            for row in rows:
               starid.append((row["Star_id"]))
            return starid

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)    	


    def get_FluxRange(self,_ra,_dec,s_time,e_time):
	 try:
	    self.cursor.execute("""  select flux,starid  from(select * FROM(SELECT * FROM (select Star_id as starid ,
                                     Exposure.Exposure_id as exposureid,_RA as _ra , _DEC as _dec, Flux as
                                     flux,ExposureTime as time   from (Star,Exposure) Where Exposure.Exposure_id =
                                     Star.EXPOSURE_ID) as tmp) as TEMP  where _ra = %s AND _dec = %s)as t where time
                                     BETWEEN %s AND %s """,(_ra,_dec,s_time,e_time))
             
            
            rows = self.cursor.fetchall()
            flux = []
            
            for row in rows:
               flux.append((row["flux"]))
            return flux

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1) 

    def getAllImagePath_AND_ExposureID(self):
         try:
            self.cursor.execute("SELECT Exposure_id,ImagePath FROM Exposure")
            rows = self.cursor.fetchall()
            ID = []
            PATH = []
            DATA = []
          
            for row in rows:
               ID.append((row["Exposure_id"]))
               PATH.append((row["ImagePath"]))

            DATA.append(ID)
            DATA.append(PATH)
            return DATA   

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    def WriteEC_INTO_Extinction(self,data):
        try:
           if len(data) == 2 : 
              EC = data[0]
              print "EC %s" % EC 
              starid = []
              starid = data[1]
              self.cursor.execute("SELECT Insert_EC(%s)",(EC))
              row = self.cursor.fetchone()
              ID = row.values()[0]
              print "ID %s" % ID
              i = 0
              while i<len(starid):
                 STARID = starid[i]
                 self.cursor.execute("SELECT Insert_Star_Extinction(%s,%s)",(STARID,ID))
                 i = i+1
 
           else:
              print "List is short"

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

    def get_Exposures(self,_ra,_dec):
        try:
            self.cursor.execute("""select ID FROM(SELECT Exposure.Exposure_id  as ID, _RA as _ra, _DEC as _dec FROM
                                   (Star,Exposure) WHERE Exposure.Exposure_id = Star.EXPOSURE_ID) as tmp WHERE _ra = %s
                                    AND _dec = %s""",(_ra,_dec))

            rows = self.cursor.fetchall()
            exposureid =[]
            for row in rows:
               exposureid.append((row["ID"]))
            return exposureid

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1]) 
            sys.exit(1)    

    def get_MagRange(self,_ra,_dec,s_time,e_time):
	 try:
	    self.cursor.execute("""  select Mag,starid  from(select * FROM(SELECT * FROM (select Star_id as starid ,
                                Exposure.Exposure_id as exposureid,_RA as _ra , _DEC as _dec, InstrMag as Mag,ExposureTime
                                as time   from (Star,Exposure) Where Exposure.Exposure_id = Star.EXPOSURE_ID) as tmp) as
                                TEMP  where _ra = %s AND _dec = %s)as t where time BETWEEN %s AND %s """
                                ,(_ra,_dec,s_time,e_time))
               
            rows = self.cursor.fetchall()
            Mag = []
            
            for row in rows:
               Mag.append((row["Mag"]))
            return Mag

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1)

    


    def add_AM (self,starid,am):
	  try:
              self.cursor.execute("SELECT COUNT(*) FROM Star WHERE Star_id = %s",(starid))
              row = self.cursor.fetchone()
              size = row.values()[0]
              flag = 0
              if size != 1 :
                  flag = -1 
              else :
                  self.cursor.execute("UPDATE Star SET AirMass = %s WHERE Star_id = %s", (am,starid))

              return flag

          except MySQLdb.Error, e:
               print "Error %d: %s" % (e.args[0],e.args[1])
               sys.exit(1)
    
    def CloseConnection(self):
          self.cursor.close()   
          self.conn.commit()
          self.conn.close()






