####################################################################
###########Extinction Coefficient Module for Chimera################
######Written by Lisette Antigua, Brandon Fink, Brandon Gilfus######
####Chris Guida, Kendall Moore, Dawn Orlandella, and Dan Schlegel###
####################################################################

####extinction.py : Handles obtaining the extinction coefficient.

#CALLING THE EXTINCTION COEFFICIENT MODULE FROM THE SCHEDULER:
#Use the ex.extinctionCoefficient(database,ra,dec,error,starttime,endtime,latitude,outname) function!

#Example code calling from the scheduler:
#ex = Extinction()
#ex.extinctionCoefficient(database('moxie.oswego.edu','dschlege','password','chimera'),320.1,69.2,.01,'2009-05-03 18:58:30','2009-05-03 18:58:50','-22:32:04.000',"test")

from seeing import Seeing 
from chimera.core.site import Site
from chimera.util.position import Position
from chimera.util.coord import Coord
from chimeradb import database
import numpy as np
import math
import os, glob, sys
import ephem

#PyFITS provides us the ability to use FITS file header data
import pyfits

#Debug mode
debugmode=0

class Extinction:
	def __init__(self):
          self.db = 0
	  self.ra = Coord.fromD(0)
	  self.dec = Coord.fromD(0)
	  self.error = 0
	  self.starttime = ''
	  self.endtime = ''
	  self.latitude = Coord.fromD(0)
	  self.outname = ""
	  self.path = ""
	  self.seeing = Seeing()


	#Returns local sidereal time from the regular time.
	def timeToLST(self,time):
	  sun = ephem.Sun()
	  obs = ephem.Observer()
	  obs.lat = self.latitude.toHMS()
	  obs.pressure = 0
	  obs.date = time
	  return obs.sidereal_time()

	#Computes the coefficient. takes arrays: flux, altitude
	def computeExtinctionCoefficient(self,flux, altitudeArr):
		#These will be needed for our output.
		magnitude = []
		airmass = []

		#Make radec a global var
		global radec

		#Iterate over each of the arrays to call computeEC
		for i in range(len(flux)):
			temparr = self.computeEC(flux[i], altitudeArr[i])
			magnitude.append(temparr[0])
			airmass.append(temparr[1])

		#Print out magnitudes
		if debugmode:
		  print "Magnitudes:"
		  print magnitude

		#Print out airmasses
		if debugmode:
		  print "Airmasses:"
		  print airmass

		#Now run a least squares fit and return the slope of the line.
		#We arent sure which order these come back in!
		m,b = np.polyfit(airmass,magnitude,1)

		#Print out m,b
		if debugmode:
		  print "M value:", m
		  print "B value:", b

		#Test plot
		self.plotViaGnuplot(self.outname,"Airmass",airmass,"Instrumental Magnitude",magnitude,m,b)

		return m

	#Compute from the array of fluxes and array of local sidereal times the extinction coefficient.
	def computeExtinctionWithLST(self,flux, lstArr):
		altArr = []
		aTuple = self.ra, self.dec
		raDec = Position(aTuple)
		for lst in lstArr:
			#this returns the altitude and azimuth
			altAz = raDec.raDecToAltAz(raDec, self.latitude, lst)
			#Get the altitude
			altArr.append(altAz.alt)
		print flux
		print altArr
		return self.computeExtinctionCoefficient(flux, altArr)

	#Compute the magnitude and airmass from specific raDec (of type Position), flux values.
	def computeEC(self,flux, altitude):
		#airmass calculation
		airmass = 1/math.cos(altitude)
		#magnitude calculation
		magnitude = 2.5*math.log(flux)
		return [magnitude,airmass]

	# Generates a data file (fileName.dat), a gnuplot batch file (fileName.gnu)
	#  and a PNG image of the plot (fileName.png)
	def plotViaGnuplot(self,fileName, x_label, x_list, y_label, y_list, m, b):
	    # Set path to the gnuplot binary
	    gpPath = "gnuplot"

	    # Set output type and file extension
	    terminalType = "png"    # Alternatives: jpeg, gif, postscript, pdf, etc.
	    extension = ".png"      # Alternatives: jpg, gif, ps, pdf, etc.

	    # Create space-delimited data file
	    file = open(fileName + ".dat", "w")
	    for i in range(len(x_list)):
		print >> file, str(x_list[i]) + ' ' + str(y_list[i])
	    file.flush()
	    file.close()

	    # Create gnuplot batch file
	    file = open(fileName + ".gnu", "w")
	    print >> file, "set terminal " + terminalType
	    print >> file, "set output \"" + fileName + extension + "\""
	    print >> file, "set xlabel \"" + x_label + "\""
	    print >> file, "set ylabel \"" + y_label + "\""
	    print >> file, "set xrange [ " + str(min(x_list) - 1) + " : " + str(max(x_list) + 1) + " ]"
	    print >> file, "set yrange [ " + str(min(y_list) - 1) + " : " + str(max(y_list) + 1) + " ]"
	    print >> file, "set mxtics 5"
	    print >> file, "set mytics 5"
	    print >> file, "set xtics " + str((max(x_list) - min(x_list)) / 5)
	    print >> file, "set ytics " + str((max(y_list) - min(y_list)) / 5)
	    print >> file, "f(x) = " + str(m) + " * x + " + str(b)
	    print >> file, "plot f(x) notitle with lines, \"" + fileName + ".dat\" using 1:2 notitle"
	    file.flush()
	    file.close()

	    # Run gnuplot, passing in the batch file
	    os.system(gpPath + " " + fileName + ".gnu")


	def doFileModeEC(self,path):
	  self.path = path
	  #Initial setup variables, these will be passed to CalculateExtinctionCoefficient
	  fluxArr = []
	  altArr = []
	  for infile in glob.glob( os.path.join(path, '*.fits') ):
	    print "current file is: " + infile
	    #Read the Altitude from the FITS file
	    hdulist = pyfits.open(infile)
	    altCoord = Coord.fromHMS(hdulist[0].header['ALT'])
	    altArr.append(altCoord.toR())
	    #Set the latitude. This really only needs to be done once though.
	    latitude = Coord.fromHMS(hdulist[0].header['LATITUDE'])
	    #Get the RA and DEC for this star
	    ra = Coord.fromHMS(hdulist[0].header['RA'])
	    dec = Coord.fromHMS(hdulist[0].header['DEC'])
	    #Run the file through seeing
	    self.seeing.run(infile)
	    star = self.seeing.getStarClosestTo(ra, dec)
	    fluxArr.append(self.seeing.getFlux(star))
	  if debugmode:
	    print fluxArr
	    print altArr
	  print "Extinction Coefficient: " + str(self.computeExtinctionCoefficient(fluxArr, altArr))
	##END doFileModeEC()


	def doDatabaseModeEC(self,db):
	  fluxArr = []
	  lstArr = []
	  #Pull the data from the database, make sure our ra and dec are in Degrees.
	  data = db.getTimeAndFlux(self.ra,self.dec,self.error,self.starttime,self.endtime)
	  for time,flux in data:
	    #reformat the time to something ephem likes.
	    time = str(time.year) + '/' + str(time.month) + '/' + str(time.day) + " " + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
	    lstArr.append(self.timeToLST(time))
	    fluxArr.append(flux)
	  coeff = self.computeExtinctionWithLST(fluxArr, lstArr)
	  #Insert into database
	  sid = db.get_StarID(self.ra.toD(),self.dec.toD())
	  db.WriteEC_INTO_Extinction([coeff,sid])
	##END doDatabaseModeEC()



	#This would be called from the scheduluer!
	#ra1 and dec1 are Coord objects (Be sure to convert to degrees)
	#Latitude is a coord object in HMS
	#Start and End time are in the format 2009-05-03 18:58:30 (standard python datetime format)
	#dbase is an already initialized database object.
	def extinctionCoefficient(self,dbase,ra1,dec1,error,startTime1,endTime1,latitude1,outfile):
	  outname = outfile
	  self.ra = Coord.fromD(ra1)
	  self.dec = Coord.fromD(dec1)
	  self.error = error
	  self.starttime = startTime1
	  self.endtime = endTime1
	  self.latitude = Coord.fromHMS(latitude1)
	  self.outname = outfile
	  self.doDatabaseModeEC(dbase)
##END CLASS EXTINCTION
