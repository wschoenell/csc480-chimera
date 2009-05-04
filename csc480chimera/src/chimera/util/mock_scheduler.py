#! /usr/bin/python


from runAstrometryNet import AstrometryNet
__author__="sdoherty"
__date__ ="$May 1, 2009 12:12:12 PM$"

if __name__ == "__main__":
    print "Starting Mock Scheduler";
    print"========================\n"
    try:
        print "* (1 of 3) Calling Astrometry.net script for directory of images."
        #single image
        #img_path = "tests/480/image/image.fits"
        #image = AstrometryNet.path_2_image(img_path)

        #batch of image
        directorypath = "tests/480/batch/"
        AstrometryNet.add_image_directory_to_queue(directorypath)
        AstrometryNet.print_queue()
        AstrometryNet.solve_queue()

        
        #print "testing ra and dec check."
        #AstrometryNet.confirm_ra_dec_by_image_center(image)
        print "finished mock scheduler stage 1 processing."
    except Exception, e:
        print e
    try:
        print "\n* (2 of 3) Calling Seeing script for directory of images."
    except Exception, e:
        print e

    try:
        print "\n* (3 of 3) Calling Extinction script for directory of images."
    except Exception, e:
        print e