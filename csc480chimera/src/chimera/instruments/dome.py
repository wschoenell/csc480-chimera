#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# chimera - observatory automation system
# Copyright (C) 2006-2007  P. Henrique Silva <henrique@astro.ufsc.br>
# Copyright (C) 2006-2007  Antonio Kanaan <kanaan@astro.ufsc.br>

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

import logging
import time
import sys
import Queue

from chimera.core.chimeraobject import ChimeraObject

from chimera.interfaces.dome import IDome
from chimera.interfaces.dome import Mode

from chimera.core.event    import event
from chimera.core.lock    import lock
from chimera.core.callback import callback

from chimera.core.exceptions import ObjectNotFoundException
from chimera.core.exceptions import ChimeraException

from chimera.util.coord import Coord


__all__ = ['Dome']


class Dome(ChimeraObject, IDome):

    def __init__(self):
        ChimeraObject.__init__(self)

        self.queue = Queue.Queue()
        self._mode = None

        # to reuse telescope proxy on control method
        self._controlTel = None
        self._controlDrv = None
        # to cache for az_resolution of the dome
        self.controlAzRes = None

    def __start__(self):

        # connect events with driver
        drv = self.getDriver()
        drv.ping()
        
        drv.slewBegin    += self.getProxy()._slewBeginClbk
        drv.slewComplete  += self.getProxy()._slewCompleteClbk
        drv.abortComplete += self.getProxy()._abortCompleteClbk
        drv.slitOpened    += self.getProxy()._slitOpenedClbk
        drv.slitClosed    += self.getProxy()._slitClosedClbk

        self.setHz(1/4.0)

        if self["mode"] == Mode.Track:
            self.track ()
        elif self["mode"] == Mode.Stand:
            self.stand ()
        else:
            self.log.warning ("Invalid dome mode: %s. Will use Stand mode instead.")
            self.stand ()

        # telescope events
        self._connectTelEvents()

        return True

    def __stop__ (self):

        if self['park_on_shutdown']:

            try:
                self.stand()
                self.log.info("Parking the dome...")
                self.slewToAz(self['park_pos'])
            except Exception, e:
                self.log.warning('Unable to park dome: %s', str(e))

        if self['close_on_shutdown'] and self.isSlitOpen():
            try:
                self.log.info("Closing the slit...")
                self.closeSlit()
            except Exception, e:
                self.log.warning('Unable to close dome: %s', str(e))
        
        # disconnect events
        drv = self.getDriver()
        
        drv.slewBegin     -= self.getProxy()._slewBeginClbk
        drv.slewComplete  -= self.getProxy()._slewCompleteClbk
        drv.abortComplete -= self.getProxy()._abortCompleteClbk
        drv.slitOpened    -= self.getProxy()._slitOpenedClbk
        drv.slitClosed    -= self.getProxy()._slitClosedClbk

        self._disconnectTelEvents()
        return True


    def _connectTelEvents (self):
        
        try:
            tel = self.getTelescope()

            tel.slewBegin    += self.getProxy()._telSlewBeginClbk
            tel.slewComplete  += self.getProxy()._telSlewCompleteClbk
            tel.abortComplete += self.getProxy()._telAbortCompleteClbk

        except ObjectNotFoundException:
            self.log.warning("Couldn't found telescope."
                                "Telescope events would not be monitored.")

        return True

    def _disconnectTelEvents (self):
        try:
            tel = self.getTelescope()
            
            tel.slewBegin    -= self.getProxy()._telSlewBeginClbk
            tel.slewComplete  -= self.getProxy()._telSlewCompleteClbk
            tel.abortComplete -= self.getProxy()._telAbortCompleteClbk

        except ObjectNotFoundException:
            pass

        return True

    def _reconnectTelEvents (self):
        self._disconnectTelEvents()
        self._connectTelEvents()

    # callbacks
    def _slewBeginClbk(self, position):
        if not isinstance(position, Coord):
            position = Coord.fromDMS(position)

        self.slewBegin(position)
        
    def _slewCompleteClbk(self, position):
        if not isinstance(position, Coord):
            position = Coord.fromDMS(position)

        self.slewComplete(position)

    def _abortCompleteClbk(self, position):
        if not isinstance(position, Coord):
            position = Coord.fromDMS(position)

        self.abortComplete(position)

    def _slitOpenedClbk(self, position):
        if not isinstance(position, Coord):
            position = Coord.fromDMS(position)

        self.slitOpened(position)

    def _slitClosedClbk(self, position):
        if not isinstance(position, Coord):
            position = Coord.fromDMS(position)

        self.slitClosed(position)

    # telescope callbacks
    def _telSlewBeginClbk (self, target):
        if self.getMode() != Mode.Track: return

        self.log.debug("[event] telescope slewing to %s." % target)
        
    def _telSlewCompleteClbk (self, target):
        if self.getMode() != Mode.Track: return

        tel = self.getTelescope()
        self.log.debug("[event] telescope slew complete, new position=%s." % target)

    def _telAbortCompleteClbk (self, position):
        if self.getMode() != Mode.Track: return

        tel = self.getTelescope()
        self.log.debug("[event] telescope aborted last slew, new position=%s." % position)


    # utilitaries
    def getDriver(self):
        return self.getManager().getProxy(self['driver'], lazy=True)        
        
    def getTelescope(self):
        return self.getManager().getProxy(self['telescope'], lazy=True)        

    def control (self):

        if self.getMode() == Mode.Stand:
            return True

        if not self.queue.empty():
            self.log.debug("[control] processing queue... %d item(s)." % self.queue.qsize())
            self._processQueue()
            return True

        try:

            if not self._controlTel:
                self._controlTel = self.getTelescope()

            if self._controlTel.isSlewing():
                    self.log.debug("[control] telescope slewing... not checking az.")
                    return True

            self._telescopeChanged(self._controlTel.getAz())

        except ObjectNotFoundException:
            raise ChimeraException("Couldn't found the selected telescope."
                                    " Dome cannnot track.")

        return True

    def _telescopeChanged (self, az):

        if not isinstance(az, Coord):
            az = Coord.fromDMS(az)

        if self._needToMove(az):
            self.log.debug("[control] adding %s to the queue." % az)
            self.queue.put(az)
        else:
            self.log.debug("[control] telescope still in the slit, standing"
                            " (dome az=%.2f, tel az=%.2f, delta=%.2f.)" % (self.getAz(), az, abs(self.getAz()-az)))


    def _needToMove (self, az):
        if not self._controlDrv:
            self._controlDrv = self.getDriver()

        if not self.controlAzRes:
            self.controlAzRes = self._controlDrv["az_resolution"]
            
        return abs(az - self._controlDrv.getAz()) >= self.controlAzRes

    def _processQueue (self):
        
        if self.queue.empty(): return

        while not self.queue.empty():

            target = self.queue.get()
            try:
                self.log.debug("[queue] slewing to %s" % target)
                self.slewToAz(target)
            finally:
                self.log.debug("[queue] slew to %s complete" % target)                
                self.queue.task_done()
        
    @lock
    def track(self):
        if self.getMode() == Mode.Track: return

        self._reconnectTelEvents()
        
        tel = self.getTelescope()
        self.log.debug("[mode] tracking...")
        self._telescopeChanged(tel.getAz())

        self._mode = Mode.Track

    @lock
    def stand(self):
        self._processQueue()
        self.log.debug("[mode] standing...")
        self._mode = Mode.Stand

    @lock
    def sync(self):
        self._processQueue()

    def getMode(self):
        return self._mode

    @lock
    def slewToAz (self, az):

        if not isinstance(az, Coord):
            az = Coord.fromDMS(az)

        if int(az) >= 360:
            az = az % 360
        
        drv = self.getDriver()
        drv.slewToAz (az)

    def isSlewing (self):
        drv = self.getDriver()
        return drv.isSlewing ()
    
    def abortSlew (self):
        drv = self.getDriver()
        drv.abortSlew ()

    @lock
    def getAz (self):
        drv = self.getDriver()
        return drv.getAz ()

    @lock
    def openSlit (self):
        drv = self.getDriver()
        drv.openSlit()

    @lock
    def closeSlit (self):
        drv = self.getDriver()
        drv.closeSlit()

    def isSlitOpen (self):
        drv = self.getDriver()
        return drv.isSlitOpen()
    
    def getMetadata(self, request):
        if self.isSlitOpen():
            slit = 'Open'
        else:
            slit = 'Closed'
        return [
                ('DOME_MDL', str(self['model']), 'Dome Model'),
                ('DOME_TYP', str(self['type']), 'Dome Type'),
                ('DOME_TRK', str(self['mode']), 'Dome Tracking/Standing'),
                ('DOME_SLT', str(slit), 'Dome slit status'),
                ] + self.getDriver().getMetadata(request)
