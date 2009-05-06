
from chimera.util.astrometry_net import AstrometryNet

if __name__ == "__main__":
    print "Starting Mock Scheduler";
    print"========================\n"
    try:
        print "* (1) Calling Astrometry.net script for directory of images."
        
        #batch of image
        directorypath = "tests/480/batch/"
        AstrometryNet.add_image_directory_to_queue(directorypath)
        AstrometryNet.print_queue()
        AstrometryNet.solve_queue()        
        
        print "finished mock scheduler stage 1 processing."
    except Exception, e:
        print e
        
    try:
        print "* (2) Calling Astrometry.net script for directory of images."
        #single image
        img_path = "tests/480/image/image.fits"
        image = AstrometryNet.path_2_image(img_path)

        print "testing ra and dec check."
        AstrometryNet.confirm_ra_dec_by_image_center(image)
        print "finished mock scheduler stage 1 processing."
    except Exception, e:
        print e

  