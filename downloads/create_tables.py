# create_tables.py - Creates tables from database
import sys
import MySQLdb

try:
   conn = MySQLdb.connect(host = "localhost",user = "root",passwd = 
   "modha",db = "test_db")
except MySQLdb.Error,e:
 print "Error %d: %s" %(e.args[0],e.args[1])
 sys.exit(1)

# create table Exposure,Star,Relation,Extinction,StarData 

try:
   cursor = conn.cursor()
   cursor.execute("""CREATE TABLE IF NOT EXISTS Exposure
                   (Exposure_id Integer UNSIGNED AUTO_INCREMENT Primary key not NULL,
                    ExposureTime TIMESTAMP,
                    Global_RA Double not NULL,
                    Global_DEC Double not NULL,
                    ImagePath LongText, 
                    Filter Text,
                    SkyFlux Double)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS Star
                   (Star_id Integer UNSIGNED AUTO_INCREMENT Primary key not NULL,
                    StarName varchar(100),  
                    _RA Double not NULL,
                    _DEC Double not NULL,
                    _AM Double)""") 
   cursor.execute("""CREATE TABLE IF NOT EXISTS Relation
                   (STAR_ID Integer not NULL,
                    EXPOSURE_ID Integer not NULL,
                    FOREIGN KEY (STAR_ID)
                    REFERENCES Star(Star_id),
                    FOREIGN KEY (EXPOSURE_ID)
                    REFERENCES Exposure(Exposure_id))""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS StarData
                   (Starid Integer not NULL,
                    _Time TIMESTAMP not NULL,
                    StarFlux Double,
                    FWHM Double,
                    InstruMag Double, 
                    FOREIGN KEY (Starid)
                    REFERENCES Star(Star_id))""") 
   cursor.execute("""CREATE TABLE IF NOT EXISTS Extinction 
                   (Star_ID Integer not NULL,
                    Extinction_ID Integer UNSIGNED AUTO_INCREMENT Primary key not NULL,
                    Start_Time TIMESTAMP not NULL,
                    End_Time TIMESTAMP not NULL,
                    Ext_Coe Double not NULL,
                    FOREIGN KEY (Star_ID)
                    REFERENCES Star(Star_id))""") 
   cursor.execute("""ALTER TABLE Exposure AUTO_INCREMENT = 101010""")
   cursor.execute("""ALTER TABLE Star AUTO_INCREMENT = 201010""")
   cursor.execute("""ALTER TABLE Extinction AUTO_INCREMENT = 301010""")
   

except MySQLdb.Error, e:
 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)
cursor.close()
conn.commit()
conn.close ()
  
