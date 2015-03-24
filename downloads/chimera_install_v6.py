#!/usr/bin/python

NUMPY_HTTP = "http://superb-east.dl.sourceforge.net/sourceforge/numpy/numpy-1.2.1.tar.gz"
NUMPY_FILE = NUMPY_HTTP.split("/")[-1]
PYRO_HTTP = "http://internap.dl.sourceforge.net/sourceforge/pyro/Pyro-3.8.1.tar.gz"
PYRO_FILE = PYRO_HTTP.split("/")[-1]
PYYAML_HTTP = "http://pyyaml.org/download/pyyaml/PyYAML-3.08.tar.gz"
PYYAML_FILE = PYYAML_HTTP.split("/")[-1]
DATEUTIL_HTTP = "http://labix.org/download/python-dateutil/python-dateutil-1.4.1.tar.gz"
DATEUTIL_FILE = DATEUTIL_HTTP.split("/")[-1]
SETUPTOOLS_HTTP = "http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c9.tar.gz"
SETUPTOOLS_FILE = SETUPTOOLS_HTTP.split("/")[-1]
PYEPHEM_HTTP = "http://pypi.python.org/packages/source/p/pyephem/pyephem-3.7.3.3.tar.gz"
PYEPHEM_FILE = PYEPHEM_HTTP.split("/")[-1]
SWIG_HTTP = "http://superb-east.dl.sourceforge.net/sourceforge/swig/swig-1.3.37.tar.gz"
SWIG_FILE = SWIG_HTTP.split("/")[-1]

import random
import os
import sys
import textwrap

print "Chimera Observatory Automation System Installation\n"
if os.getuid() != 0:
	print "This script must be run as root."
	print "Type 'man sudo' for more details."
	sys.exit(0)
initialOut = "This script uses aptitude to verify that all necessary packages are installed.  If a package is missing it will be installed without user intervention.  Running this script will over write any previous Chimera installation.  Please read the following carefully as if they are not present they will be downloaded and installed once you have  confirmed you would like to install Chimera." 
print textwrap.fill(initialOut)
print "\nDependencies:"
print "  - Python-dev"
print "  - Subversion"
print "  - GCC"
print "  - Make"
print "  - Wget"
print "  - GNU Tar"
print "  - NumPy"
print "  - Pyro"
print "  - PyYAML"
print "  - SetupTools"
print "  - DateUtil"
print "  - PyEphem"
print "  - G++"
print "  - Swig"
print "  - libusb-dev"

if not raw_input("\nDo you want to install Chimera and all it's dependencies? [y/n] ").startswith("y"):
	sys.exit(0)

tmpFolder = ".chimera-install-" + str(random.randint(100000,999999))
os.system("mkdir " + tmpFolder)
os.chdir(tmpFolder)

print "Checking for Python-dev..."
os.system("apt-get install python-dev -yqq")

print "Checking for Subversion..."
os.system("apt-get install subversion -yqq")

print "Checking for GCC..."
os.system("apt-get install gcc -yqq")

print "Checking for Make..."
os.system("apt-get install make -yqq")

print "Checking for Wget..."
os.system("apt-get install wget -yqq")

print "Checking for GNU Tar..."
os.system("apt-get install tar -yqq")

print "Checking for Pyro (Python Remote Objects)..."
try:
	import Pyro
except:
	os.system("wget " + PYRO_HTTP)
	os.system("tar -xf " + PYRO_FILE)
	os.chdir(PYRO_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("./setup.py build")
	os.system("./setup.py install")
	os.chdir("..")

print "Checking for PyYAML..."
try:
	import yaml
except:
	os.system("wget " + PYYAML_HTTP)
	os.system("tar -xf " + PYYAML_FILE)
	os.chdir(PYYAML_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("python setup.py build")
	os.system("python setup.py install")
	os.chdir("..")

print "Checking for SetupTools..."
try:
	import setuptools
except:
	os.system("wget " + SETUPTOOLS_HTTP)
	os.system("tar -xf " + SETUPTOOLS_FILE)
	os.chdir(SETUPTOOLS_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("./setup.py build")
	os.system("./setup.py install")
	os.chdir("..")

print "Checking for DateUtil..."
try:
	import dateutil
except:
	os.system("wget " + DATEUTIL_HTTP)
	os.system("tar -xf " +  DATEUTIL_FILE)
	os.chdir(DATEUTIL_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("./setup.py build")
        os.system("./setup.py install")
	os.chdir("..")

print "Checking for PyEphem..."
try:
	import ephem
except:
	os.system("wget " + PYEPHEM_HTTP)
	os.system("tar -xf " + PYEPHEM_FILE)
	os.chdir(PYEPHEM_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("python setup.py install")
	os.chdir("..")

print "Checking for G++..."
os.system("apt-get install g++ -yqq")

print "Checking for NumPy..."
try:
	import numpy
except:
	os.system("wget " + NUMPY_HTTP)
	os.system("tar -xf " + NUMPY_FILE)
	os.chdir(NUMPY_FILE.split("/")[0].split(".tar.gz")[0])
	os.system("./setup.py config")
	os.system("./setup.py build")
	os.system("./setup.py install")
	os.chdir("..")

print "Downloading and installing Swig..."
os.system("wget " + SWIG_HTTP)
os.system("tar -xf " + SWIG_FILE)
os.chdir(SWIG_FILE.split("/")[0].split(".tar.gz")[0])
os.system("./configure")
os.system("make")
os.system("make install")
os.chdir("..")

print "Checking for libusb-dev"
os.system("apt-get install libusb-dev -yqq")

print "Downloading Chimera from the Google Code SVN Repository"
#os.system("svn checkout http://chimera.googlecode.com/svn/trunk/ chimera-read-only")
os.system("svn checkout http://csc480-chimera.googlecode.com/svn/trunk/ csc480-chimera-read-only")
os.chdir("csc480-chimera-read-only/csc480chimera")
os.system("./setup.py install")
os.chdir("../../")
os.system("rm -rf " + tmpFolder)
