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

import time
import random
import threading

from chimera.interfaces.telescopedriver import ITelescopeDriverSlew
from chimera.interfaces.telescopedriver import ITelescopeDriverSync
from chimera.interfaces.telescopedriver import ITelescopeDriverPark
from chimera.interfaces.telescopedriver import ITelescopeDriverTracking
from chimera.interfaces.telescopedriver import SlewRate

from chimera.core.chimeraobject         import ChimeraObject

from chimera.core.lock import lock
from chimera.core.site import Site

from chimera.util.coord    import Coord
from chimera.util.position import Position


class FakeTelescope (ChimeraObject,
                     ITelescopeDriverSlew,
                     ITelescopeDriverSync,
                     ITelescopeDriverPark,
                     ITelescopeDriverTracking):
    
    __config__ = {'site':   '/Site/0'}
    
    def __init__ (self):
        ChimeraObject.__init__(self)

        self.__slewing = False
        self._az  = Coord.fromDMS(0)
        self._alt = Coord.fromDMS(70)

        self._slewing  = False
        self._tracking = True
        self._parked   = False
        
        self._abort = threading.Event()
        
        try:
            self._site = self.getManager().getProxy(self['site'])
            self._gotSite=True
        except:
            self._site = Site()
            self._gotSite=False
        
        self._setRaDecFromAltAz()
    
    def _getSite(self):
        if self._gotSite:
            self._site._transferThread()
            return self._site
        else:
            try:
                self._site = self.getManager().getProxy(self['site'])
                self._gotSite=True
            except:
                pass
        return self._site
    
    def _setRaDecFromAltAz(self):
        raDec=self._getSite().altAzToRaDec(Position.fromAltAz(self._alt, self._az))
        self._ra=raDec.ra
        self._dec=raDec.dec

    def _setAltAzFromRaDec(self):
        altAz=self._getSite().raDecToAltAz(Position.fromRaDec(self._ra, self._dec))
        self._alt=altAz.alt
        self._az=altAz.az

    def __start__ (self):
        self.setHz(1)

    @lock
    def control (self):
        self._getSite()
        if not self._slewing:
            if self._tracking:
                self._setAltAzFromRaDec()
            else:
                self._setRaDecFromAltAz()                                                          
        return True

    def open(self):
        pass

    def close(self):
        pass

    def ping(self):
        pass

    @lock
    def slewToRaDec(self, position):

        self.slewBegin(position)

        ra_steps = position.ra - self.getRa()
        ra_steps = float(ra_steps/10.0)

        dec_steps = position.dec - self.getDec()
        dec_steps = float(dec_steps/10.0)

        self._slewing = True
        self._abort.clear()

        t = 0
        while t < 5:

            if self._abort.isSet():
                self._slewing = False
                return

            self._ra  += ra_steps
            self._dec += dec_steps
            self._setAltAzFromRaDec()
            
            time.sleep(0.5)
            t += 0.5
        
        self._slewing = False
            
        self.slewComplete(self.getPositionRaDec())

    @lock
    def slewToAltAz(self, position):
        self.slewBegin(self._getSite().altAzToRaDec(position))

        alt_steps = position.alt - self.getAlt()
        alt_steps = float(alt_steps/10.0)

        az_steps = position.az - self.getAz()
        az_steps = float(az_steps/10.0)

        self._slewing = True
        self._abort.clear()

        t = 0
        while t < 5:

            if self._abort.isSet():
                self._slewing = False
                return

            self._alt  += alt_steps
            self._az += az_steps
            self._setRaDecFromAltAz()
            
            time.sleep(0.5)
            t += 0.5
        
        self._slewing = False
            
        self.slewComplete(self.getPositionRaDec())


    def isSlewing (self):
        return self._slewing

    def abortSlew(self):
        self._abort.set()
        while self.isSlewing():
            time.sleep(0.1)

        self.abortComplete(self.getPositionRaDec())

    @lock
    def moveEast(self, offset, rate=SlewRate.MAX):
        pass

    @lock
    def moveWest(self, offset, rate=SlewRate.MAX):
        pass

    @lock
    def moveNorth(self, offset, rate=SlewRate.MAX):
        pass

    @lock
    def moveSouth(self, offset, rate=SlewRate.MAX):
        pass

    def getRa(self):
        return self._ra

    def getDec(self):
        return self._dec

    def getAz(self):
        return self._az

    def getAlt(self):
        return self._alt

    def getPositionRaDec(self):
        return Position.fromRaDec(self.getRa(), self.getDec())

    def getPositionAltAz(self):
        return Position.fromAltAz(self.getAlt(), self.getAz())

    def getTargetRaDec(self):
        return Position.fromRaDec(self.getRa(), self.getDec())

    def getTargetAltAz(self):
        return Position.fromAltAz(self.getAlt(), self.getAz())

    #GUI Compatibility methods
    def getAlignMode(self):
        return self['align_mode']
 
    def getLat(self):
        return self._getSite()['latitude']

    def getLong(self):
        return self._getSite()['longitude']
    
    def getDate(self):
        return self._getSite().ut()

    def getLocalTime(self):
        return self._getSite().localtime()
    
    def getUTCOffset(self):
        return self._getSite()['utc_offset']
    
    def getLocalSiderealTime(self):
        return self._getSite().LST()
    
    def getCurrentTrackingRate(self):
        pass

    @lock
    def sync(self, position):
        self._ra  = position.ra
        self._dec = position.dec

    @lock
    def park(self):
        self._parked = True

    @lock
    def unpark(self):
        self._parked = False

    def isParked(self):
        return self._parked

    @lock
    def setParkPosition (self, position):
        pass

    def startTracking (self):
        self._tracking = True
    
    def stopTracking (self):
        self._tracking = False

    def isTracking (self):
        return self._tracking
