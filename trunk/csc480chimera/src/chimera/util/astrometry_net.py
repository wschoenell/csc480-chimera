#! /usr/bin/python

from chimera.core.exceptions import ChimeraException
from chimera.util.image import Image

import logging
import os
import os.path
import shutil
import subprocess
from subprocess import Popen

from database.chimeradb import database

log = logging.getLogger(__name__)



class AstrometryNet():
    image_queue = [];#array of images to solve

  #============================== QUEUE METHODS ==============================
    @staticmethod
    def print_queue():
        """Prints the contents of the image_queue: mainly for debug purposes"""
        for image in AstrometryNet.image_queue:
            print image

    @staticmethod
    def add_image_directory_to_queue(directorypath):
        """Adds all fits images to image processing queue to be processed:
        Does not start processing function"""
        for f in os.listdir(directorypath):
            AstrometryNet.add_image_to_queue(directorypath + f)

    @staticmethod
    def add_image_to_queue(imagepath):
        """Adds a single image to the image queue for processing
        Does not start processing function"""
        global image_queue
        pathname, filename = os.path.split(imagepath)
        pathname = pathname + "/"
        basefilename, file_xtn = os.path.splitext(filename)

        # *** enforce .fits extension
        if (file_xtn != ".fits"):
            return
        # *** check whether the file exists or not
        if (os.path.exists(imagepath) == False):
            return
        image = Image.fromFile(imagepath)
        AstrometryNet.image_queue.append(image)

    @staticmethod
    def solve_queue():
        """Processes each fits image in the image queue through Astrometry.net"""
        index = 0
        count = len(AstrometryNet.image_queue)
        for img in AstrometryNet.image_queue:
            index = index + 1
            print "\n\n=============================>Solving image %d of %d" % (index, count)
            new_img_path = AstrometryNet.solve_field_by_file(img)
            AstrometryNet.save_to_database(new_img_path)

#==============================UTILITIES ==============================
    @staticmethod
    def path_2_image(fullfilename):
        """Create a Chimera image object from a path name"""
        print "     creating image from file name"
        image = Image.fromFile(fullfilename)
        return image

    @staticmethod
    def is_fits(image):
        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        pathname = pathname + "/"
        basefilename, file_xtn = os.path.splitext(filename)

        # *** enforce .fits extension
        if (file_xtn != ".fits"):
            return False
        else:
            return True

    @staticmethod
    def print_image_info(image):
        """Documentation"""
        try:
            ra = image["CRVAL1"]    # expects to see this in image
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")
        try:
            dec = image["CRVAL2"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")
        width = image["NAXIS1"]
        height = image["NAXIS2"]
        radius = 5.0 * abs(image["CD1_1"]) * width
        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
            # SHOW USER WHAT CURRENT FILE RA AND DEC ARE
        print "\n+------THE IMAGE YOU TOOK CONTAINS--------------"
        print "|	path name: " + pathname
        print "|	file name: " + fullfilename
        print "|	ra       : %f" % (ra)
        print "|	dec      : %f" % (dec)
        print "|	height   : %f" % (height)
        print "|	width    : %f" % (width)
        print "|	radius   : %f" % (radius)
        print "+-----------------------------------------------"


#============================== SOLVE METHODS ==============================
    @staticmethod
    def solve_field_by_path(fullfilename):
        """
        @param: fullfilename entire path to image
        @type: str
        Does astrometry to image=fullfilename
        Uses astrometry.net as its star finder
        """
        image = AstrometryNet.path_2_image(fullfilename)
        solve_field_by_file(image)

    @staticmethod
    def solve_field_by_file(image):
        """
        @param: image the fits image to be processed
        @type: Image

        Does astrometry to image=fullfilename
        Uses astrometry.net as its star finder

        """
        print "     Solving image : %s" % image
        AstrometryNet.print_image_info(image)

        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name         = os.path.basename(filename)
        # @type name str
        root_name = name.replace(".fits", "", 1)
        is_solved    = pathname + "/" + root_name + ".solved"
        wcs_imgname  = pathname + "/" + root_name + ".new"
        wcs_solution = pathname + "/" + root_name + ".wcs"
        #print "base image name: %s" % name

        print "\n\n+------SENDING TO ASTROMETRY.NET----------------"
        line = "/usr/local/astrometry/bin/solve-field --guess-scale --overwrite %s"  % fullfilename
        print "|     commandline = %s" % line
        print "|     Starting solving"
        solve = Popen(line.split())
        solve.wait()

        #print "%s" % is_solved
        # if solution failed, there will be no file .solved
        if (os.path.exists(is_solved) == False):
            print "|     Astrometry.net could not find a solution for image: %s " % (image)

        # *.new will be the old fits file with the new header
        shutil.copyfile(wcs_solution, wcs_solution + ".fits")
        if (os.path.exists(wcs_imgname) == True):
            print "|     astrometry.net has produced a new fits file " + wcs_imgname
            print "|     which contains the wcs header added to the original fits image "
        print "|\n+------ASTROMETRY.NET FINISHED------------------\n\n"
        return(wcs_imgname)

    #============================== DATABASE METHODS ==============================

    @staticmethod
    def save_to_database(fullfilename):
        """Saves global RA and DEC and image path to database"""
        abs_path = os.path.abspath(fullfilename)
        print "     Saving to database %s" %abs_path

        wcs_image = AstrometryNet.path_2_image(abs_path)
        G_RA = AstrometryNet.get_center_ra(wcs_image)
        G_DEC = AstrometryNet.get_center_dec(wcs_image)
        new_file_name = wcs_image.filename()
        mydb = database()
        result = mydb.add_Exposure(new_file_name, G_RA, G_DEC)
        if (result > 0):
            print "     Image path, global RA and global DEC saved to database "



#==============================CALCULATING FROM CENTER OF IMAGE ==============================
    @staticmethod
    def get_center_ra(image):
        """Documentation"""
        fullfilename = image.filename()
        line = "/usr/local/astrometry/bin/wcsinfo %s"  % fullfilename
        solve = Popen(line.split(), stdout=subprocess.PIPE)#pipe the output to alternate stdout
        stdout, stdin = solve.communicate(None)#grab the piped output into the variable str
        solve.wait()
        result_array = stdout.split("\n")
        for et in result_array:
            # @type et str
            if(et.startswith("ra_center ")):
                txt, ra_center = et.split()
        return ra_center

    @staticmethod
    def get_center_dec(image):
        """Documentation"""
        fullfilename = image.filename()
        line = "/usr/local/astrometry/bin/wcsinfo %s"  % fullfilename

        solve = Popen(line.split(), stdout=subprocess.PIPE)#pipe the output to alternate stdout
        stdout, stdin = solve.communicate(None)#grab the piped output into the variable str
        solve.wait()
        result_array = stdout.split("\n")
        for et in result_array:
            # @type et str
            if(et.startswith("dec_center ")):
                txt, dec_center = et.split()
        return dec_center

    @staticmethod
    def confirm_ra_dec_by_image_center(image):
        """Takes a fits image as input.
        Based on the center of the image, this method compares the ra
        and dec of the input image with the ra and dec of the world coordinate
        system header produced by Astrometry.net and returns true if image header
        matches within some tolerance and false otherwise.
        """
        if(AstrometryNet.is_fits(image) == False):
            print "     Image was not a .fits file cannot process"
            return


        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name = os.path.basename(filename)
        root_name = name.replace(".fits", "", 1)
        wcs_new = pathname + "/" + root_name + ".new"
        wcs_solution = pathname + "/" + root_name + ".solved"

        # if solution failed, there will be no file .wcs
        if (os.path.exists(wcs_solution) == False):
            print "     Astrometry.net not solved yet starting to solve"
            AstrometryNet.solve_field_by_file(image)
        else:
            print "     File already solved."
        print "     File solved starting confirmation."


        #print "     SOLUTION %s" % wcs_solution
        if (os.path.exists(wcs_new) == True):
            wcs_image = AstrometryNet.path_2_image(wcs_new)
        else:
            print "     Astrometry.net could not find a solution exiting ra and dec check"
            return

        ra_center = AstrometryNet.get_center_ra(image)
        dec_center = AstrometryNet.get_center_dec(image)
        print "\n+------YOUR IMAGE HEADER SAYS-----------+"
        print "|    ra_center       : %s" % (ra_center)
        print "|    dec_center      : %s" % (dec_center)
        print "|"
        wcs_ra = AstrometryNet.get_center_ra(wcs_image)
        wcs_dec = AstrometryNet.get_center_dec(wcs_image)
        print "+------ASTROMETRY.NET SAYS IT IS--------+"
        print "|    ra_center       : %s" % (wcs_ra)
        print "|    dec_center      : %s" % (wcs_dec)
        print "+---------------------------------------+"
        ra_center  = float(ra_center)
        dec_center = float(dec_center)
        wcs_ra     = float(wcs_ra)
        wcs_dec    = float(wcs_dec)
        raflag = False
        decflag = False
        tolerance = 0.5
        tol = tolerance / 2
        if(ra_center >= wcs_ra - tol and ra_center <= wcs_ra + tol):
            raflag = True
            print "|    ra within range = True"
        else:
            print "|    ra within range = True"
        if(dec_center >= wcs_dec -tol and dec_center <= wcs_dec + tol):
            decflag = True
            print "|    dec within range = True"
        else:
            print "|    dec within range = True"
        if(raflag and decflag):
            print "|    image within tolerance = True"
            print "+---------------------------------------+"
            return  True
        else:
            print "|    image within tolerance = False"
            print "+---------------------------------------+"
            return False


#==============================CALCULATING FROM REFERENCE PIXEL ==============================
    @staticmethod
    def get_referencepixel_ra(fullfilename):
        """Processes each fits image in the image queue through Astrometry.net"""
        image = AstrometryNet.path_2_image(fullfilename)
        ra = image["CRVAL1"]
        return ra

    @staticmethod
    def get_referencepixel_dec(fullfilename):
        """Processes each fits image in the image queue through Astrometry.net"""
        image = AstrometryNet.path_2_image(fullfilename)
        dec = image["CRVAL2"]
        return dec

    @staticmethod
    def confirm_ra_dec_by_reference_pixel(image):
        """Takes a fits image as input.
        Based on the reference pixel CRVAL1, CRVAL2 this method compares the ra
        and dec of the input image with the ra and dec of the world coordinate
        system header produced by Astrometry.net and returns true if image header
        matches within some tolerance and false otherwise.
        """
        #TODO:  WARNING:
        #TODO:  This method is not reliable, because it is not certain that the reference pixel of the input img header
        #TODO:  corresponds to the same location in space as the reference pixel in the Astrometry.net wcs header
        #TODO:  therefore, whatever transformations are necessary, need to be done to make this workan
        try:
            source_image_ra = image["CRVAL1"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")
        try:
            source_image_dec = image["CRVAL2"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")

        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name = os.path.basename(filename)
        root_name = name.replace(".fits", "", 1)
        wcs_new = pathname + "/" + root_name + ".new"
        wcs_solution = pathname + "/" + root_name + ".solved"

       # if solution failed, there will be no file .wcs
        if (os.path.exists(wcs_solution) == False):
            print "     Astrometry.net not solved yet starting to solve"
            AstrometryNet.solve_field_by_file(image)
        else:
            print "     File already solved."
        print "     File solved starting confirmation."

        #print "     SOLUTION %s" % wcs_solution
        if (os.path.exists(wcs_new) == True):
            wcs_image = AstrometryNet.path_2_image(wcs_new)
        else:
            print "     Astrometry.net could not find a solution exiting ra and dec check"
            return

        print "\n+------YOUR IMAGE HEADER SAYS-----------+"
        print "|    ra_center       : %s" % (source_image_ra)
        print "|    dec_center      : %s" % (source_image_dec)
        print "|"

        try:
            wcs_ra  = wcs_image["CRVAL1"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")
        try:
            wcs_dec = wcs_image["CRVAL2"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")

        print "+------ASTROMETRY.NET SAYS IT IS--------+"
        print "|    ra_center       : %s" % (wcs_ra)
        print "|    dec_center      : %s" % (wcs_dec)
        print "+---------------------------------------+"
        ra_center  = float(ra_center)
        dec_center = float(dec_center)
        wcs_ra     = float(wcs_ra)
        wcs_dec    = float(wcs_dec)
        raflag = False
        decflag = False
        tolerance = 0.5
        tol = tolerance / 2
        if(ra_center >= wcs_ra - tol and ra_center <= wcs_ra + tol):
            raflag = True
            print "|    ra within range = True"
        else:
            print "|    ra within range = True"
        if(dec_center >= wcs_dec -tol and dec_center <= wcs_dec + tol):
            decflag = True
            print "|    dec within range = True"
        else:
            print "|    dec within range = True"
        if(raflag and decflag):
            print "|    image within tolerance = True"
            print "+---------------------------------------+"
            return  True
        else:
            print "|    image within tolerance = False"
            print "+---------------------------------------+"
            return False

class AstrometryNetException(ChimeraException):
    pass

class NoSolutionAstrometryNetException(ChimeraException):
    pass


if __name__ == "__main__":
    try:
        print "Test run of Astrometry.net script\n"
        img_path = "tests/480/image/image.fits"

        #print "Testing image queue."
        #AstrometryNet.add_image_directory_to_queue("tests/480/batch/")
        #AstrometryNet.add_image_to_queue("tests/480/test1/1/landolt-SA112223-0001.fits")
        #AstrometryNet.print_queue()
        #AstrometryNet.solve_queue()

        print "1. starting photometry processing."
        image = AstrometryNet.path_2_image(img_path)

        print "2. testing ra and dec check."
        print "     withing tolerance = %s " % AstrometryNet.confirm_ra_dec_by_image_center(image)

        print "3. testing database"
        AstrometryNet.save_to_database(img_path)

        print "finished processing."
    except Exception, e:
        print e



