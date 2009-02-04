#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# chimera - observatory automation system
# Copyright (C) 2006-2007  P. Henrique Silva <henrique@astro.ufsc.br>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import threading
import time
import Pyro.util

from chimera.core.chimeraobject import ChimeraObject
from chimera.interfaces.camera import (ICameraExpose, ICameraTemperature, ICameraInformation)

from chimera.controllers.imageserver.imagerequest import ImageRequest

from chimera.core.exceptions import ChimeraValueError

from chimera.core.lock import lock


class Camera (ChimeraObject,
              ICameraExpose, ICameraTemperature, ICameraInformation):

    def __init__(self):
        ChimeraObject.__init__(self)

        self.abort = threading.Event()
        self.abort.clear()

    def getDriver(self):
        """
        Get a Proxy to the instrument driver. This function is necessary '
        cause Proxies cannot be shared among different threads.
        So, every time you need a driver Proxy you need to call this to
        get a Proxy to the current thread.
        """
        return self.getManager().getProxy(self['driver'], lazy=True)        
        
    def __start__ (self):

        drv = self.getDriver()

        # connect callbacks to driver events
        drv.exposeBegin       += self.getProxy()._exposeBeginDrvClbk        
        drv.exposeComplete    += self.getProxy()._exposeCompleteDrvClbk
        drv.readoutBegin      += self.getProxy()._readoutBeginDrvClbk
        drv.readoutComplete   += self.getProxy()._readoutCompleteDrvClbk        
        drv.abortComplete     += self.getProxy()._abortDrvClbk
        drv.temperatureChange += self.getProxy()._tempChangeDrvClbk

        return True

    def __stop__ (self):
        
        if self.isExposing():
            self.abortExposure(False)
            while self.isExposing():
                time.sleep(1)
        
        # disconnect our callbacks
        drv = self.getDriver()

        drv.exposeBegin       -= self.getProxy()._exposeBeginDrvClbk        
        drv.exposeComplete    -= self.getProxy()._exposeCompleteDrvClbk
        drv.readoutBegin      -= self.getProxy()._readoutBeginDrvClbk
        drv.readoutComplete   -= self.getProxy()._readoutCompleteDrvClbk        
        drv.abortComplete     -= self.getProxy()._abortDrvClbk
        drv.temperatureChange -= self.getProxy()._tempChangeDrvClbk

    def _exposeBeginDrvClbk (self, request):
        self.exposeBegin(request)
    
    def _exposeCompleteDrvClbk (self, request):
        self.exposeComplete(request)

    def _readoutBeginDrvClbk (self, request):
        self.readoutBegin(request)
    
    def _readoutCompleteDrvClbk (self, request):
        self.readoutComplete(request)

    def _abortDrvClbk (self):
        self.abortComplete()
    
    def _tempChangeDrvClbk (self, temp, delta):
        self.temperatureChange(temp, delta)

    @lock
    def expose (self, request=None, **kwargs):

        if request:

            if isinstance(request, ImageRequest):
                imageRequest = request
            elif isinstance(request, dict):
                imageRequest = ImageRequest(**request)
        else:
            if kwargs:
                imageRequest = ImageRequest(**kwargs)
            else:
                imageRequest = ImageRequest()
        
        frames = imageRequest['frames']
        interval = imageRequest['interval']

        if frames == 1:
            interval = 0.0

        # clear abort setting
        self.abort.clear()

        # config driver
        drv = self.getDriver()

        images = []

        for frame_num in range(frames):
            
            if self.abort.isSet():
                return images
            
            imageRequest.fetchPreHeaders(self.getManager())
            image = drv.expose(imageRequest)
            images.append(image)
            
            if interval > 0 and frame_num < frames:
                time.sleep(interval)

        return tuple(images)
                
    def abortExposure (self, readout=True):
        drv = self.getDriver()
        drv.abortExposure()

        return True
    
    def isExposing (self):
        drv = self.getDriver()
        return drv.isExposing()

    @lock
    def startCooling (self, tempC):
        drv = self.getDriver()
        drv.startCooling(tempC)
        return True

    @lock
    def stopCooling (self):
        drv = self.getDriver()
        drv.stopCooling()
        return True

    def isCooling (self):
        drv = self.getDriver()
        return drv.isCooling()

    @lock
    def getTemperature(self):
        drv = self.getDriver()
        return drv.getTemperature()

    @lock
    def getSetPoint(self):
        drv = self.getDriver()
        return drv.getSetPoint()

    @lock
    def startFan(self, rate=None):
        drv = self.getDriver()
        return drv.startFan(rate)

    @lock
    def stopFan(self):
        drv = self.getDriver()
        return drv.stopFan()

    def isFanning(self):
        drv = self.getDriver()
        return drv.isFanning()

    
    def getMetadata(self, request):
        drv = self.getDriver()
        return [
                ('CAMERA', str(self['camera_model']), 'Camera Model'),
                ('CCD',    str(self['ccd_model']), 'CCD Model'),
                ('CCD_DIMX', drv.getPhysicalSize()[0], 'CCD X Dimension Size'),
                ('CCD_DIMY', drv.getPhysicalSize()[1], 'CCD Y Dimension Size'),
                ('CCDPXSZX', drv.getPixelSize()[0], 'CCD X Pixel Size [micrometer]'),
                ('CCDPXSZY', drv.getPixelSize()[1], 'CCD Y Pixel Size [micrometer]')]  + drv.getMetadata(request)
                #('XBINNING', int(request.binning[0]), 'Readout CCD Binning (x-axis)'),
                #('YBINNING', int(request.binning[-1]), 'Readout CCD Binning (y-axis)'),
                #('IMAGETYP', request['type'], 'Image type')]

    def getCCDs(self):
        drv = self.getDriver()
        return drv.getCCDs()

    def getCurrentCCD(self):
        drv = self.getDriver()
        return drv.getCurrentCCD()

    def getBinnings(self):
        drv = self.getDriver()
        return drv.getBinnings()

    def getADCs(self):
        drv = self.getDriver()
        return drv.getADCs()

    def getPhysicalSize(self):
        drv = self.getDriver()
        return drv.getPhysicalSize()

    def getPixelSize(self):
        drv = self.getDriver()
        return drv.getPixelSize()

    def getOverscanSize(self, ccd=None):
        drv = self.getDriver()
        return drv.getOverscanSize()

    def supports(self, feature=None):
        drv = self.getDriver()
        return drv.supports(feature)


