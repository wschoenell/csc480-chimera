"""
this code is from:  http://imac-252a.stanford.edu/programs/Python/Pyraf_Routine.py
"""

#! /usr/bin/env python

##This script will execute the IRAF DAOFIND program on all of the files in
##the current working directory [.../2005-05-1*/ShackHartman/Raw] and 
##put the results in a MySQL database.
##
##The Database name is DAOFIND and the table for each date is given by
##	0[Month]_[Date]
##
##The entries in the DATABASE ARE 
###N XCENTER   YCENTER   MAG      SHARPNESS   SROUND      GROUND      ID         
import sys,os
from pyraf import iraf 
import pyfits
from numarray import *
from pylab import *
import MySQLdb
import get_date

#GET THE DATE
Date=get_date.get_date1()
Year=Date[0]
Month=Date[1]
Day=Date[2]
exam_date='1_31'

CPdir='/nfs/slac/g/ki/ki08/lsst/CPanalysis/'+Year+'-'+Month+'-'+Day+'/ShackHartman/'
stats_exists=os.path.exists(CPdir+'stats_'+exam_date+'/')
coo_exists=os.path.exists(CPdir+'coo_'+exam_date+'/')
if coo_exists:
	os.rmdir(CPdir+'coo_'+exam_date+'/')
else:
	os.mkdir(CPdir+'coo_'+exam_date+'/')
mag_exists=os.path.exists(CPdir+'mag_'+exam_date+'/')
if mag_exists:
        os.rmdir(CPdir+'mag_'+exam_date+'/')
else:
        os.mkdir(CPdir+'mag_'+exam_date+'/')


#GET ALL OF THE RAW FILENAMES IN CWD
raw_filenames=iraf.files('h*5132*.fits',Stdout=1)
num_files=len(raw_filenames)
##Open up the connection and include some error handling
try:
        conn=MySQLdb.connect (host="localhost",
                              user="root",
                              passwd="mysql",
                              db="my_test")
except MySQLdb.Error, e:
        print "Error $d: $s" % (e.args[0],e.args[1])
        sys.exit
                                                                                
##CREATE CURSOR OBJECT
cursor=conn.cursor()
                                                                                
try:
        cursor.execute("CREATE DATABASE DAOFIND_PHOT")
        print "Database Created"
except MySQLdb.Error, e:
        print e
	print "Database DAOFIND exists: Moving ON"


try:
        cursor.execute("use DAOFIND_PHOT");
        cursor.execute('CREATE TABLE DAOFIND_'+exam_date+'_'+Month+'_'+Day+
                                               '(Filename varchar(20),'+
                                               'XCOORD float,'+
                                               'YCOORD float,'+
                                               'MAG float,'+
                                               'SHARPNESS float,'+
                                               'SROUND float,'+
					       'GROUND float,'+
					       'ID mediumint);')
except MySQLdb.Error, e:
        print e

try:
        cursor.execute("use DAOFIND_PHOT");
        cursor.execute('CREATE TABLE PHOT_'+exam_date+'_'+Month+'_'+Day+
                                               '(Filename varchar(20),'+
                                               'XCOORD float,'+
                                               'YCOORD float,'+
                                               'XERR float,'+
                                               'YERR float,'+
                                               'MAG float,'+
                                               'FLUX float,'+
                                               'AREA float,'+
					       'ID mediumint);')

except MySQLdb.Error, e:
        print e
                                      

#PREPARE THE GRID
subx=2*arange(25)-25
xrow=12.5*subx+542
suby=arange(25)-12
ycol=25.0*suby+465

y=repeat(ycol,25,axis=0)
y.shape=(25,25)
x=zeros((25,25))
x[:,:]=xrow

y.shape=(625,1)
x.shape=(625,1)

#Import the good packages from IRAF
iraf.digiphot(_doprint=0)
iraf.daophot(_doprint=0)

#DATAPARS
datapars=iraf.datapars.getParList()
findpars=iraf.findpars.getParList()
centerpars=iraf.centerpars.getParList()

#SET SOME PARTICULAR 
iraf.centerpars.setParam('cbox','10.0')
iraf.datapars.setParam('fwhmpsf','5.8')
iraf.datapars.setParam('datamax','10000')
iraf.datapars.setParam('datamin','-100')
iraf.findpars.setParam('threshold','80')
iraf.centerpars.saveParList(filename='~/iraf/uparm/datcentes.par')
iraf.datapars.saveParList(filename='~/iraf/uparm/datdataps.par')

#Set up daofind to go without prompting for input
iraf.daofind.setParam('image','@all_fits_files.txt')	#Set filename
iraf.daofind.setParam('output','../coo_'+exam_date+'/')
iraf.daofind.setParam('verify','no')			#Don't verify
iraf.daofind.saveParList(filename='daofind.par')	#Save values


for i in range(num_files-1):
	
	#DAOFIND------------------------------------------------------------
	iraf.daofind.setParam('image',raw_filenames[i])
	daostring=iraf.daofind(mode='h',Stdout=1)	#Run DAOFIND hidden
	lendaostring=len(daostring)			#Get Number of Spots
	print lendaostring

	filename=daostring[1].split()[1]		#Get Filename


	for spot in range(3,lendaostring-3):
		cursor.execute("INSERT INTO DAOFIND_"+exam_date+'_'+
			       Month+'_'+Day+
			       " VALUES('"+
			       filename+"','"+      
			       daostring[spot].split()[0]+"','"+
                               daostring[spot].split()[1]+"','"+
                               daostring[spot].split()[2]+"','"+
                               daostring[spot].split()[3]+"','"+
                               daostring[spot].split()[4]+"','"+
                               daostring[spot].split()[5]+"','"+
                               daostring[spot].split()[6]+
			       "')")

	#PHOT---------------------------------------------------------------
	iraf.phot.setParam('image',raw_filenames[i])
	iraf.phot.setParam('coords','../coo_'+exam_date+'/')
	iraf.phot.setParam('output','../mag_'+exam_date+'/'+raw_filenames[i]+'.mag.1')
	iraf.phot.setParam('verify','no')
	photstring=iraf.phot(mode='h',Stdout=1)
                                                                                
	lenphotstring=len(photstring)
	print lenphotstring
	print photstring[0].split()[0]
	print photstring[0].split()[1]
	print photstring[0].split()[2]
	print photstring[0].split()[3]
	print photstring[0].split()[4]
	print photstring[0].split()[5]
  	iraf.txdump('../mag_'+exam_date+'/'+raw_filenames[i]+'.mag.1',
		    "xcenter,ycenter,xerr,yerr,mag,flux,area",'yes',
	            Stdout='../mag_'+exam_date+'/'+raw_filenames[i]+'.mag.1.txt')	
	txstr=iraf.txdump('../mag_'+exam_date+'/'+raw_filenames[i]+'.mag.1',
                    "xcenter,ycenter,xerr,yerr,mag,flux,area",'yes',
                    Stdout=1)
	lentxdump=len(txstr)
	print txstr[1]
	print len(txstr[1])

	for spot in range(1,lentxdump-1):
	      
		xcoord=float(txstr[spot].split()[0])
		ycoord=float(txstr[spot].split()[1])
		index_check=where((abs(x-xcoord) < 11) &
				  (abs(y-ycoord) < 11))
		if index_check[0].nelements()==0: 
			index=-1
		else:
		   	index=index_check[0][0]
 
                cursor.execute("INSERT INTO PHOT_"+exam_date+'_'+
			       Month+'_'+Day+
                               " VALUES('"+
                               filename+"','"+
                               txstr[spot].split()[0]+"','"+
                               txstr[spot].split()[1]+"','"+
                               txstr[spot].split()[2]+"','"+
                               txstr[spot].split()[3]+"','"+
                               txstr[spot].split()[4]+"','"+
                               txstr[spot].split()[5]+"','"+
                               txstr[spot].split()[6]+"','"+
			       str(index)+
                               "')")


