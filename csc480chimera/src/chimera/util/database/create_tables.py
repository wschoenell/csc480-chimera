# create_tables.py - Creates tables from database
import sys
import MySQLdb

try:
   conn = MySQLdb.connect(host = "localhost",user = "modha",passwd = 
   "802528907",db = "chimera")
except MySQLdb.Error,e:
 print "Error %d: %s" %(e.args[0],e.args[1])
 sys.exit(1)


try:
   cursor = conn.cursor()
   cursor.execute("""CREATE TABLE IF NOT EXISTS Exposure
                   (Exposure_id Integer AUTO_INCREMENT Primary key not NULL,
                    ExposureTime TIMESTAMP,
                    LocalSideralTime varchar(20), 
                    ImagePath LongText, 
		    G_RA Double,
		    G_DEC Double,		
                    Filter Text,
                    SkyFlux Double)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS Star
                   (Star_id Integer AUTO_INCREMENT Primary key not NULL,
                    StarName varchar(100),  
                    _RA Double not NULL,
                    _DEC Double not NULL,
                    Flux Double,
                    FWHM Double,
                    InstrMag Double,
                    AirMass Double,
                    EXPOSURE_ID Integer not NULL,
                    FOREIGN KEY (EXPOSURE_ID)
                    REFERENCES Exposure(Exposure_id))""") 
   cursor.execute("""CREATE TABLE IF NOT EXISTS Star_Extinction
                   (Extinction_id Integer not NULL,
		    Starid Integer not NULL,
		    FOREIGN KEY (Starid)
                    REFERENCES Star(Star_id),
            	    FOREIGN KEY (Extinction_id)
                    REFERENCES Star(Extinction_ID))""") 
   cursor.execute("""CREATE TABLE IF NOT EXISTS Extinction
                   (Extinction_id Integer AUTO_INCREMENT Primary key not NULL,
		    Extinction_COE Double not NULL)""") 
   cursor.execute("""ALTER TABLE Exposure AUTO_INCREMENT = 101010""")
   cursor.execute("""ALTER TABLE Star AUTO_INCREMENT = 201010""")
   cursor.execute("""ALTER TABLE Extinction AUTO_INCREMENT = 301010""")
   
except MySQLdb.Error, e:
 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)
cursor.close()
conn.commit()
conn.close ()
  

