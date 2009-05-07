####################################################################
###########Extinction Coefficient Module for Chimera################
######Written by Lisette Antigua, Brandon Fink, Brandon Gilfus######
####Chris Guida, Kendall Moore, Dawn Orlandella, and Dan Schlegel###
####################################################################

####extinctioncoefficient.py : Handles running the extinction coefficient from the command line
####extinction.py : Contains the functions for calculating the extinction coefficient. If you are calling directly, look there!

#USING THE EXTINCTION COEFFICIENT MODULE FROM THE COMMAND LINE:
#python extinctioncoefficient.py [-f:<path to images> | ra=<RA> dec=<DEC> s=<Start Time> e=<End Time> l=<Latitude>] -o:<Image output filename>
#		      		 [-s:<server address> -d:<database> -u:<username> -p:<password>]
#Times should be in this format: 2009-05-03 18:58:30 (python datetime standard)
#Latitude is in HMS, RA and DEC are in Degrees
#Using the path to images will read the fits file headers for RA, DEC and altitude. 
#Using the DB will read the LST from the DB and calculate ext. coeff from there.

#Example code calling from the command line with DB:
#python extinctioncoefficient.py ra=320.1 dec=69.2 s=2009-05-03 18:58:30 e=2009-05-03 18:58:50 l=-22:32:04.000 -o:test -d:chimera -u:dschlege -p:password -s:moxie.oswego.edu

#Example code calling from the command line with file output:
#python extinctioncoefficient.py -f:images/


from extinction import Extinction
from chimeradb import database
from chimera.util.coord import Coord
import os, glob, sys
#from seeing import Seeing 

#This sets latitude, we need to pull this from the fits or DB, default is the brazil telescope.
latitude = Coord.fromHMS('-22:32:04.000')

#Default to DB mode
filemode=0
db=0
dbserver=0
dbname=0
dbuser=0
dbpass=0


#Default output filename
outname="extinction"

#Default error in RA and DEC
error = 0

#Command processing
last = ''

for arg in sys.argv:
  if arg.startswith("-f:"): #find if this is folder search.
    path=arg.lstrip("-f:")
    filemode=1
  elif arg.startswith("ra="):
    ra=arg.lstrip("ra=")
  elif arg.startswith("dec="):
    dec=arg.lstrip("dec=")
  elif arg.startswith("s="):
    starttime=arg.lstrip("s=")
    last='s'
  elif arg.startswith("e="):
    endtime=arg.lstrip("e=")
    last='e'
  elif arg.startswith("-o:"):
    outname=arg.lstrip("-o:")
  elif arg.startswith("l="):
    latitude=arg.lstrip("l=")
  elif arg.startswith("-s:"):
    dbserver=arg.lstrip("-s:")
  elif arg.startswith("-d:"):
    dbname=arg.lstrip("-d:")
  elif arg.startswith("-u:"):
    dbuser=arg.lstrip("-u:")
  elif arg.startswith("-p:"):
    dbpass=arg.lstrip("-p:")
  else:
    if last=='s':
      starttime += ' ' + arg
    elif last=='e':
      endtime += ' ' + arg

ex = Extinction()

if filemode:
  ex.doFileModeEC(path)
else:
  ex.extinctionCoefficient(database(dbserver,dbuser,dbpass,dbname),ra,dec,error,starttime,endtime,latitude,outname)

