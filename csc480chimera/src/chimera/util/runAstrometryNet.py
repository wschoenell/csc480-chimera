import os.path

from chimera.core.exceptions import ChimeraException
from chimera.util.image import Image
from chimera.util.database import DatabaseInterface
import logging
import os
import shutil
import subprocess
from subprocess import Popen
log = logging.getLogger(__name__)

class AstrometryNet():
    image_queue = [];#array of images to solve

        
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
        for img in AstrometryNet.image_queue:
            AstrometryNet.solve_field_by_file(img)
            
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
    def path_2_image(fullfilename):
        """Documentation"""
        image = Image.fromFile(fullfilename)
        return image

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
        print "-------THE IMAGE YOU TOOK CONTAINS-------"
        print "	path name: " + pathname
        print "	file name: " + fullfilename
        print "	ra       : %f" % (ra)
        print "	dec      : %f" % (dec)
        print "	height   : %f" % (height)
        print "	width    : %f" % (width)
        print "	radius   : %f" % (radius)

    @staticmethod
    def save_to_databse(G_RA, G_DEC, fullfilename):
        """Saves global RA and DEC and image path to database"""
        database.insertINTOExposure(G_RA, G_DEC, fullfilename)

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
        AstrometryNet.print_image_info(image)        

        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name         = os.path.basename(pathname)
        is_solved    = pathname + "/.solved"
        wcs_imgname  = pathname + "/" + name + ".new"
        wcs_solution = pathname + "/" + name + ".wcs"


        # if it is already there, make sure to delete it
        if (os.path.exists(is_solved)):
            print "solved indicator exists: deleting it now..."
            os.remove(is_solved)
        print "-------SENDING TO ASTROMETRY.NET-------"
        line = "/usr/local/astrometry/bin/solve-field --guess-scale --overwrite %s"  % fullfilename
        print "commandline = %s" % line
        solve = Popen(line.split())
        solve.wait()

        # if solution failed, there will be no file .solved
        if (os.path.exists(is_solved) == False):
            print "Astrometry.net could not find a solution for image: %s %s" % (image, is_solved)

        # *.new will be the old fits file with the new header
        shutil.copyfile(wcs_solution, wcs_solution + ".fits")
        if (os.path.exists(wcs_imgname) == True):
            print "astrometry.net has produced a new fits file " + wcs_imgname
        return(wcs_imgname)

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
    def confirm_ra_dec_by_reference_pixel(image):
        """takes a fits image and returns true if image header matches within some
            tolerance of the header created by astrometry.net
        """   
        try:
            source_image_ra = image["CRVAL1"]    # expects to see this in image
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")
        try:
            source_image_dec = image["CRVAL2"]
        except:
            raise AstrometryNetException("Need CRVAL1 and CRVAL2 and CD1_1 on header")

        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name         = os.path.basename(pathname)
        is_solved    = pathname + "/" + name + ".solved"
        wcs_solution = pathname + "/" + name + ".wcs"
        wcs_image = AstrometryNet.path_2_image(wcs_solution)
        
        
        # if solution failed, there will be no file .solved
        if (os.path.exists(is_solved) == False):
            print "Astrometry.net not solved yet starting to solve"
            print is_solved
            AstrometryNet.solve_field_by_file(image)

        print "-------YOUR IMAGE HEADER SAYS     -------"
        print "	ra       : %f" % (source_image_ra)
        print "	dec      : %f" % (source_image_dec)
        wcs_ra = AstrometryNet.get_ra(wcs_image)
        wcs_dec = AstrometryNet.get_dec(wcs_image)
        print "-------ASTROMETRY.NET SAYS IT IS  -------"
        print "	ra       : %f" % (wcs_ra)
        print "	dec      : %f" % (wcs_dec)
        
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
        """takes a fits image and returns true if image header matches within some
            tolerance of the header created by astrometry.net
            USE WCSINFO
        """
        if(AstrometryNet.is_fits(image) == False):
            print "Image was not a .fits file"
            return
        # if solution failed, there will be no file .solved
        fullfilename = image.filename()
        pathname, filename = os.path.split(fullfilename)
        name         = os.path.basename(pathname)
        wcs_solution = pathname + "/" + name + ".wcs"
        
        # if solution failed, there will be no file .wcs
        if (os.path.exists(wcs_solution) == False):
            print "Astrometry.net not solved yet starting to solve"
            AstrometryNet.solve_field_by_file(image)
        if (os.path.exists(wcs_solution) == True):
            wcs_image = AstrometryNet.path_2_image(wcs_solution)
        else:
            print "Astrometry.net could not find a solution exiting ra and dec check"
            return
        ra_center = AstrometryNet.get_center_ra(image)
        dec_center = AstrometryNet.get_center_dec(image)
        print "-------YOUR IMAGE HEADER SAYS     -------"
        print "ra_center       : %s" % (ra_center)
        print "dec_center      : %s" % (dec_center)
        print ""
        wcs_ra = AstrometryNet.get_center_ra(wcs_image)
        wcs_dec = AstrometryNet.get_center_dec(wcs_image)
        print "-------ASTROMETRY.NET SAYS IT IS  -------"
        print "ra_center       : %s" % (wcs_ra)
        print "dec_center      : %s" % (wcs_dec)



class AstrometryNetException(ChimeraException):
    pass

class NoSolutionAstrometryNetException(ChimeraException):
    pass


if __name__ == "__main__":  
    try:
        img_path = "tests/480/image/image.fits"
        #print "Testing image queue."
        #AstrometryNet.add_image_directory_to_queue("tests/480/batch/")
        #AstrometryNet.add_image_to_queue("tests/480/test1/1/landolt-SA112223-0001.fits")
        #AstrometryNet.print_queue()

        #print "starting photometry processing."
        #AstrometryNet.solve_queue()
        image = AstrometryNet.path_2_image(img_path)
        print "testing ra and dec check."
        AstrometryNet.confirm_ra_dec_by_image_center(image)

        #x = AstrometryNet.solveField("tests/480/test1/1/landolt-SA112223-0001.fits",findstarmethod="astrometry.net")
        print "finished processing."
    except Exception, e:
        print e

