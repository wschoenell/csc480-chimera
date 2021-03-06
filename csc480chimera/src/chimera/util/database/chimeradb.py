#!/usr/bin/python
import sys
import MySQLdb
class database :
    conn = None
    cursor = None
    def __init__(self,Host,usr,pwd,dbname):
       try:
         self.conn = MySQLdb.connect(Host,usr,pwd,dbname)
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
            self.cursor.execute("""  select flux,time  from(select * FROM(SELECT * FROM (select Star_id as starid ,
                                     Exposure.Exposure_id as exposureid,_RA as _ra , _DEC as _dec, Flux as
                                     flux,ExposureTime as time   from (Star,Exposure) Where Exposure.Exposure_id =
                                     Star.EXPOSURE_ID) as tmp) as TEMP  where _ra = %s AND _dec = %s)as t where time
                                     BETWEEN %s AND %s """,(_ra,_dec,s_time,e_time))
            

            rows = self.cursor.fetchall()
            flux = []
            time = []
            for row in rows:
               flux.append((row["flux"]))
               time.append((row["time"]))  
            return flux

         except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0],e.args[1])
             sys.exit(1) 
              
    def getTimeAndFlux(self,_ra,_dec,error,s_time,e_time):
	 try:
	    self.cursor.execute("""  SELECT ExposureTime,Flux FROM Exposure E JOIN Star 
				     WHERE (ExposureTime BETWEEN %s AND %s) AND 
				     (_RA BETWEEN %s AND %s) AND 
				     (_DEC BETWEEN %s AND %s) """,(s_time,e_time,_ra-error/2,_ra+error/2,_dec-error/2,_dec+error/2))
            
            rows = self.cursor.fetchall()
            ret = []
            
            for row in rows:
	       aTuple = row["ExposureTime"],row["Flux"]
               ret.append(aTuple)
            return ret

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
               
               
#test = database("localhost","modha","802528907","chimera")
#print ("Flux for Starid 201015: %s") % test.get_Flux("201015")
#print ("FWHM for Starid 201015: %s") % test.get_FWHM("201015")
#print ("Magnitude for Starid 201015: %s") % test.get_Magnitude("201015")
#print ("AirMass for Starid 201015: %s") % test.get_AirMass ("201015")
#print ("Inseting data into Exposure Table : %s")% test.add_Exposure("usr/data/pic90","89.01","668.99")
#print ("Inserting data into Star Table : %s")% test.add_Star("122.34","122.44","99.10","0.005","-98.11","101012")
#print ("Inserting AirMass for Starid 201050 : %s")% test.add_AM("201050","0.7111")
#print ("List of Starid for ra = 122.34 &  dec = 122.44   : %s")% test.get_StarID("122.34","122.44")
#print ("List of Exposureid for ra = 122.34 &  dec = 122.44   : %s")% test.get_Exposures("122.34","122.44")#
#print ("ImagePath for Exposure_id 101013 : %s")% test.get_ImagePath("101013")
#print ("Exposure-id  for ImagePath /usr/data/ : %s")%test.get_ExposureID("usr/data/pic100")
#test.get_ExposureID("usr/data/pic100")
#print ("Flux for ra = 122.34, dec = 122.44, start-time = 2009-05-03 18:58:40, endtime = 2009-05-04 07:47:18 %s")% test.get_FluxRange("122.34","122.44","2009-05-03 18:58:40","2009-05-04 07:47:18")
#print ("Magnitude for ra = 122.34, dec = 122.44, start-time = 2009-05-03 18:58:40, endtime = 2009-05-04 07:47:18 %s")% test.get_MagRange("122.34","122.44","2009-05-03 18:58:40","2009-05-04 07:47:18")
#print ("List of All ImagePath & Exposure-ID's are :%s")%  test.getAllImagePath_AND_ExposureID()

