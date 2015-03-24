#! /usr/bin/env python

##This script will attempt to run DAOFIND on a file and return the values
##That I want in a reasonable fashion

import sys,os
from pyraf import iraf
import pyfits
from numarray import *
from pylab import *

#Import the good packages from IRAF
iraf.digiphot(_doprint=0)
iraf.daophot(_doprint=0)

#PYRAF uses same template and uparm parameter files as IRAF
#They can be held in memory.
#Three types of files
#	_defaultParList=default (after task is unlearned this remains)
#	_runningPartList=set used when task is run
#	_currentParList=contains updates after running a task
#	                generally agrees with uparm file
#
#If task is updated using Python syntax, the uparm copy will not be updated
#unless keyword _save=1 was specifiedi

#Two simple ways to get entire parameter list updated in uparm copy
#	1-Run epar and click on "SAVE"
#	2-in script mode saveParList() method for the task

#Four methods for getting and setting params
#	1-getParam()		2-setParam()
#	3-
#
print iraf.daofind.getParam('image',prompt=0)
iraf.daofind.setParam('image','hr5132a_001_raw.fits')
print iraf.daofind.getParam('image')
iraf.daofind.saveParList(filename='daofind.par')
iraf.daofind.getParam('verify',prompt=1)
iraf.daofind(ParList="daofind.par")
#iraf.daofind(mode="h")









#from: http://stsdas.stsci.edu/pyraf/doc.old/pyraf_guide/node2.html
"""
2 Writing Python Scripts that Use IRAF/PyRAF Tasks

Here is a very simple example to show the essential components of a Python script that calls an IRAF task, in this case imstatistics. The file imstat_example.py contains the following:

    #! /usr/bin/env python

    import sys
    from pyraf import iraf

    def run_imstat(input):
        iraf.images()
        for image in input:
            iraf.imstat(image)

    if __name__ == "__main__":
        run_imstat(sys.argv[1:])

This calls imstatistics on a list of images. This can be run either from the shell or from a Python or PyRAF session. To run it from the shell, type imstat_example.py (which must have execute permission) followed by one or more image names. To run it from Python or PyRAF, first type import imstat_example; then it can be run as follows (for example): imstat_example.run_imstat(["file.fits[1]", "file.fits[2]", "file.fits[3]"]). The argument is a list, and one or more images may be specified in the list.

The statement from pyraf import iraf makes IRAF tasks in general available. The statement iraf.images() loads the images package, which contains imstatistics. If images is already loaded, then calling iraf.images() does nothing; a package may be loaded any number of times. The run_imstat() function accepts a list of images and runs the imstatistics task (abbreviated as imstat) on each of them.

Like many IRAF tasks, imstatistics accepts a ``file name template'' as input, i.e. a string containing one or more image names, separated by commas, and possibly making use of wildcard characters. An alternative to running imstat separately on each image is to construct such a string containing all the image names, and to call imstat just once, with that string as input. Here is another version of run_imstat that concatenates the list elements to a comma-separated string. Other differences with this version are described below.

    def run_imstat(input):
        iraf.images(_doprint=0)
        all_exist = 1               # boolean flag
        for image in input:
            if not iraf.imaccess(image):
                all_exist = 0
                print "Error:  can't open", image
        if not all_exist:
            return
        iraf.imstat(",".join(input))

As in the previous version, iraf.images() is used to load the images package, but the _doprint=0 argument has been included to disable printing of the tasks in the package. The default for _doprint (a boolean flag) is 1; unless _doprint=0 is explicitly specified, when a package is loaded for the first time the names of the tasks in that package will be printed to the screen. Showing the tasks is OK for interactive use, but when loading a package in a script, the user wouldn't normally want to see such output. If the package is already loaded (and images may well be), then the tasks will not be shown anyway, but in general it's preferable to specify _doprint=0 when loading any package in a script.

A bit of error handling was also added to this version of run_imstat. imstat itself just prints a warning and continues if one or more of the input images do not exist. Much of the time, that may be all the error handling that is needed. Additional checking may be useful in cases where the functions being called take a lot of time or write intermediate files that would need to be cleaned up if one of the input files did not exist. The imaccess() function used in this example is actually of limited use for error checking, however. It does not catch an invalid image section, for example, and for a FITS file, the extension number is ignored. See the section on error handling for further discussion.

Frequently, one wants something even simpler than this, such as a file that just invokes one or more IRAF tasks without defining a function. For example, suppose the following is in the file simple.py:

    iraf.images()
    iraf.imstat("file.fits[1]")
    iraf.imstat("file.fits[2]")
    iraf.imstat("file.fits[3]")

Then it could be run by typing execfile("simple.py"). Commands in this file could also be executed (once) by import simple, but in order to do that the file would need to begin with the statement from pyraf import iraf. Using execfile is simpler, and it is also much easier to repeat; import can only be done once, after which you must use reload.

Here is another example, using slightly different style, and with comments that explain what is being done.

    #! /usr/bin/env python

    # This takes a range of numbers from the command line, constructs
    # the filename by appending each number to the root "ca" and appending
    # ".fits[0]", and splots the files one at a time.  It's intended as a
    # little pyraf demo script.

    import sys

    from pyraf import iraf

    # This function is invoked when running from the shell.
    def multiSplot():
        if len(sys.argv) < 2 or len(sys.argv) > 3:
            print » sys.stderr, "syntax:  runSplot.py first <last>"
            print » sys.stderr, "first..last is the range of integers (inclusive)"
            print » sys.stderr, "to append to the root name 'ca'"
            sys.exit()
        # The command-line arguments are strings; convert to integer.
        ifirst = int(sys.argv[1])
        if len(sys.argv) > 2:
            ilast = int(sys.argv[2])
        else:
            ilast = ifirst
        for i in range(ifirst, ilast+1):
            runSplot(i)

    # Use this function when running from Python or PyRAF.
    def runSplot(i, root="ca", extension=0):

        # Load packages; splot is in the onedspec package, which is in noao.
        # The special keyword _doprint=0 turns off displaying the tasks
        # when loading a package.
        iraf.noao(_doprint=0)
        iraf.onedspec(_doprint=0)

        # Construct the image name.
        imname = "%s%d.fits[%d]" % (root, i, extension)
        print imname        # just to see it

        # Set/view IRAF task parameter.
        # (This is done only to show how it can be done.)
        iraf.onedspec.splot.save_file = "splot_%s.log" % (root,)

        # Call IRAF task, and specify some parameters.
        iraf.onedspec.splot(imname, function="chebyshev", order=6)

    # Standard Python mechanism for handling tasks called from the command line
    # (see for example Martelli, Python in a Nutshell, chapter 7, "The Main
    # Program," or Beazley, Python Essential Reference, chapter 8).
    if __name__ == "__main__":
        multiSplot() 
"""
