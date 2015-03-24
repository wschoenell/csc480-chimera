# Introduction #

I wasn't aware of anyone else doing this, so I took the initiative and compiled a list of the Chimera files that have fixMe comments.


# Details #

<b>src/chimera/controllers/console/commands/object.py  (2 areas to fix)</b><br>
def complete (self, prefix, line, prefix_start, prefix_end)<br>
def <i>configHandler (self, args)</i><br>
<b>src/chimera/controllers/console/commander.py  (2 areas to fix)</b><br>
def init (self, controller)<br>
def init (self, controller)<br>
<b>src/chimera/controllers/imageserver/imagerequest.py  (1 area to fix)</b><br>
def init(self, kwargs)<br>
<b>src/chimera/controllers/scheduler/controller.py  (1 area to fix)</b><br>
def process(self, exposure)<br>
<b>src/chimera/controllers/scheduler/machine.py  (1 area to fix)</b><br>
def <i>process(self, exp)</i><br>
<b>src/chimera/controllers/autofocus.py  (2 areas to fix)</b><br>
def focus (self, target=Target.CURRENT, filter=None, exptime=None, binning=None, window=None, start=2000, end=6000, step=500, points=None, minmax=None, debug=False)<br>
def <i>findBestStarToFocus (self, catalog)</i><br>

<b>src/chimera/core/tests/test_chimera_object.py  (1 area to fix)</b><br>
def test_class_creation (self)<br>
<b>src/chimera/core/chimeraobject.py  (1 area to fix)</b><br>
def main (self)<br>
<b>src/chimera/core/cli.py  (2 areas to fix)</b><br>
def <i>startSystem (self, options, needRemoteManager=True)</i><br>
def <i>getActions(self, options)</i><br>
<b>src/chimera/core/config.py  (1 area to fix)</b><br>
def <i>readOptions (self, opt)</i><br>
<b>src/chimera/core/eventsproxy.py  (1 area to fix)</b><br>
def publish (self, topic, args, kwargs)<br>
<b>src/chimera/core/location.py  (1 area to fix)</b><br>
def parse(self, location)<br>
<b>src/chimera/core/manager.py  (1 area to fix)</b><br>
def start (self, location)<br>
<b>src/chimera/core/site.py  (1 area to fix)</b><br>
class AstroDate<br>
<b>src/chimera/core/systemconfig.py  (1 area to fix)</b><br>
def <i>loadConfig (self, buffer)</i><br>

<b>src/chimera/drivers/sbig/sbig.py  (1 area to fix)</b><br>
def control (self)<br>
<b>src/chimera/drivers/sbig/sbigdrv.py  (2 areas to fix)</b><br>
def init(self)<br>
def isLinked(self)<br>
<b>src/chimera/drivers/domelna40cm.py  (5 areas to fix)</b><br>
def slewToAz(self, az)<br>
def slewToAz(self, az)<br>
def slewToAz(self, az)<br>
def abortSlew(self)<br>
def getAz(self)<br>
<b>src/chimera/drivers/meade.py  (7 areas to fix)</b><br>
def autoAlign (self)<br>
def <i>move (self, direction, duration=1.0, slewRate = None)</i><br>
def <i>move (self, direction, duration=1.0, slewRate = None)</i><br>
def <i>stopMove (self, direction)</i><br>
def calibrateMove (self)<br>
def calibrateMove (self)<br>
def park (self)<br>
<b>src/chimera/drivers/optectcfs.py  (1 area to fix)</b><br>
def <i>setMode (self, mode)</i><br>
<b>src/chimera/drivers/theskytelescope.py  (2 area to fix)</b><br>
def getPositionRaDec (self)<br>
def getPositionAltAz (self)<br>

<b>src/chimera/instruments/tests/test_telescope.py  (1 area to fix)</b><br>
def test_park (self)<br>
<b>src/chimera/instruments/telescope.py  (4 areas to fix)</b><br>
def syncObject(self, name)<br>
def syncAltAz(self, position)<br>
def slewToRaDec(self, position)<br>
def slewToAltAz(self, position)<br>

<b>src/chimera/util/etree/ElementTree.py  (2 areas to fix)</b><br>
class <i>SimpleElementPath</i><br>
def iselement(element)<br>
<b>src/chimera/util/tests/test_coord.py  (1 area to fix)</b><br>
def test_parsing_conversion_hipparcos (self)<br>
<b>src/chimera/util/coord.py  (1 area to fix)</b><br>
def strfcoord (c, format=None, signed=True)<br>
<b>src/chimera/util/scat.py  (1 area to fix)</b><br>
def run (self, options)<br>

<b>src/scripts/chimera-cam.py  (1 area to fix)</b><br>
def eps_equal(a, b, eps=0.01)<br>