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
   cursor.execute("""
CREATE FUNCTION add_Exposure(path LongText,g_ra Double,g_dec Double)
RETURNS INT
DETERMINISTIC 
BEGIN 
DECLARE ID INT; 
DECLARE size INT;
SELECT COUNT(Exposure_id) into size FROM Exposure WHERE ImagePath = path;
  IF size > 0 THEN 
     SELECT -1 INTO ID;
  ELSE 
      INSERT INTO Exposure (G_RA,G_DEC,ImagePath,ExposureTime) VALUES (g_ra,g_dec,path,(SELECT NOW())); 
      SELECT Exposure_id INTO ID FROM Exposure WHERE ImagePath  = path;
  END IF;   

RETURN ID;
END """)

   cursor.execute("""
CREATE FUNCTION Insert_Star(_ra Double,_dec Double,_flux Double,_seeing Double,_mag Double,_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE size INT;
select count(*) INTO size FROM Exposure Where Exposure_id = _id;

IF (size) != 1  THEN
   select -1 into size; 

ELSE 
   INSERT INTO Star(_RA,_DEC,Flux,FWHM,InstrMag,Exposure_ID) VALUES (_ra,_dec,_flux,_seeing,_mag,_id);
   SELECT (count(Star_id)) INTO size from Star;

END IF;
RETURN size;
END """)
   cursor.execute("""
CREATE FUNCTION getExposureID(Path LongText)
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE id INT;
SELECT Exposure_id INTO id from Exposure Where ImagePath = Path;
RETURN id;
END """)
   cursor.execute("""
CREATE FUNCTION getImagePath(id INT)
RETURNS LongText
DETERMINISTIC
BEGIN
DECLARE path LongText;
SELECT ImagePath INTO path from Exposure Where Exposure_id = id;
RETURN path;
END """)   
   cursor.execute("""
CREATE FUNCTION getFlux(id INT)
RETURNS Double
DETERMINISTIC
BEGIN
DECLARE starflux Double;
SELECT Flux INTO starflux from Star Where Star_id = id;
RETURN starflux;
END """)    
   cursor.execute("""
CREATE FUNCTION getAM(id INT)
RETURNS Double
DETERMINISTIC
BEGIN
DECLARE am Double;
SELECT AirMass INTO am from Star Where Star_id = id;
RETURN am;
END """)
   cursor.execute("""
CREATE FUNCTION getFWHM(id INT)
RETURNS Double
DETERMINISTIC
BEGIN
DECLARE seeing Double;
SELECT  FWHM INTO seeing from Star Where Star_id = id;
RETURN seeing;
END """)
   cursor.execute("""
CREATE FUNCTION getMAG(id INT)
RETURNS Double
DETERMINISTIC
BEGIN
DECLARE mag Double;
SELECT  InstrMag INTO mag from Star Where Star_id = id;
RETURN mag;
END """)

   cursor.execute("""
CREATE FUNCTION Insert_AM (_ra Double,_dec Double,_am Double)
RETURNS INT
DETERMINISTIC 
BEGIN
DECLARE mycount INT;
UPDATE Star SET AirMass = _am WHERE _RA = _ra AND _DEC = _dec;
SELECT count(Star_id) from Star INTO mycount;
RETURN mycount;
END """)

   cursor.execute("""
CREATE FUNCTION Insert_EC (EC Double)
RETURNS INT
DETERMINISTIC 
BEGIN
DECLARE ID INT;
DECLARE SIZE INT;
INSERT INTO Extinction (Extinction_COE) VALUES (EC);
select count(id) INTO  SIZE from(select Extinction_id as id from Extinction where Extinction_COE = EC)as tmp WHERE id NOT IN (select distinct Extinction_id from Star_Extinction);

IF SIZE > 0 THEN 
 select id INTO ID from(select Extinction_id as id from Extinction where Extinction_COE = EC)as tmp WHERE id
 NOT  IN (select distinct Extinction_id from Star_Extinction);

ELSE
  select Extinction_id INTO ID from Extinction where Extinction_COE = EC; 
END IF;
RETURN id;
END """)

   cursor.execute("""
CREATE FUNCTION Insert_Star_Extinction (id INT,extinctionid INT)
RETURNS INT
DETERMINISTIC 
BEGIN
DECLARE flag INT;
DECLARE size INT;
select count(*) into flag FROM Star_Extinction  where Extinction_id = extinctionid;

IF flag > 0 THEN
  select -1 INTO size;

ELSE
  INSERT INTO Star_Extinction(Starid,Extinction_id) VALUES (id,extinctionid);
  select 1 INTO size;
END IF;
RETURN size;
END """)






except MySQLdb.Error, e:
 print "Error %d: %s" % (e.args[0],e.args[1])
 sys.exit(1)
cursor.close()
conn.commit()
conn.close ()
  

