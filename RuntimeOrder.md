# Introduction #
This is a basic description of what is run in order to get chimera started


# Details #


**/usr/bin/chimera contains**
```
#!/usr/bin/python
# EASY-INSTALL-SCRIPT: 'chimera-python==0.2.dev-r415','chimera'
__requires__ = 'chimera-python==0.2.dev-r415'
import pkg_resources
pkg_resources.run_script('chimera-python==0.2.dev-r415', 'chimera')
```


**calling it produces**
```
sdoherty@linux-laptop:/usr/bin$ chimera
15-02-2009 19:24:33.370 WARNING chimera log.py:85 Couldn't start Log System FileHandler ([Errno 13] Permission denied: '/home/sdoherty/.chimera/chimera.log')
[Errno 13] Permission denied: '/usr/bin/_pyro_vjBV-h.tmp'
Traceback (most recent call last):
  File "/usr/bin/chimera", line 5, in <module>
    pkg_resources.run_script('chimera-python==0.2.dev-r415', 'chimera')

  File "/usr/lib/python2.5/site-packages/pkg_resources.py", line 448, in run_script
    self.require(requires)[0].run_script(script_name, ns)

  File "/usr/lib/python2.5/site-packages/pkg_resources.py", line 1166, in run_script
    execfile(script_filename, namespace, namespace)

  File "/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/EGG-INFO/scripts/chimera", line 31, in <module>
    main()

  File "/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/EGG-INFO/scripts/chimera", line 27, in main
    SiteController(sys.argv).startup()

  File "/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/controllers/site/main.py", line 197, in startup
    self.manager = Manager(**self.config.chimera)

  File "/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/core/manager.py", line 152, in __init__
    self.adapter = ManagerAdapter (self, host, port)

  File "/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/core/manager.py", line 75, in __init__
    Pyro.core.initServer(banner=False)

  File "/usr/lib/python2.5/site-packages/Pyro-3.8.1-py2.5.egg/Pyro/core.py", line 875, in initServer
    Pyro.config.finalizeConfig_Server(storageCheck=storageCheck)

  File "/usr/lib/python2.5/site-packages/Pyro-3.8.1-py2.5.egg/Pyro/configuration.py", line 128, in finalizeConfig_Server
    raise IOError('no write access to PYRO_STORAGE ['+self.PYRO_STORAGE+']')

IOError: no write access to PYRO_STORAGE [/usr/bin]
Exception exceptions.AttributeError: "ManagerAdapter instance has no attribute 
'NameServer'" in <bound method ManagerAdapter.__del__ of 
<chimera.core.manager.ManagerAdapter instance at 0x9c608ac>> ignored
```


**from this may be deduced**

  1. ) the permissions of /home/sdoherty/.chimera/chimera.log need to be changed OR chimera needs to be run as root
  1. ) /usr/lib/python2.5/site-packages/pkg\_resources.py is being used to find the package
  1. ) chimera\_python-0.2.dev\_r415-py2.5.egg is being called by the startup script
  1. ) the egg contains a EGG-INFO/scripts folder that contains the startup scripts



---

### Order of files called ###
  1. /usr/bin/chimera
  1. /usr/lib/python2.5/site-packages/pkg\_resources.py
  1. /usr/lib/python2.5/site-packages/chimera\_python-0.2.dev\_r415-py2.5.egg/EGG-INFO/scripts/chimera
  1. /usr/lib/python2.5/site-packages/chimera\_python-0.2.dev\_r415-py2.5.egg/chimera/controllers/site/main.py
  1. /usr/lib/python2.5/site-packages/chimera\_python-0.2.dev\_r415-py2.5.egg/chimera/core/manager.py
  1. /usr/lib/python2.5/site-packages/Pyro-3.8.1-py2.5.egg/Pyro/core.py
  1. /usr/lib/python2.5/site-packages/Pyro-3.8.1-py2.5.egg/Pyro/configuration.py

### Explanation ###
<table border='1'>
<tbody>
<tr><th> <b>Call</b> </th><th> <b>Snippit</b> </th><th> <b>Result</b> </th></tr>



<a href='Hidden comment:  ************************* table row ************************'></a><br>
<tr>

<a href='Hidden comment: ============ call ============'></a><br>
<br>
<td valign='top'> <code>/usr/bin/chimera</code> </td>

<a href='Hidden comment: ============ snippit ============'></a><br>
<br>
<td valign='top'>
<pre><code>#!/usr/bin/python<br>
# EASY-INSTALL-SCRIPT: 'chimera-python==0.2.dev-r415','chimera'<br>
__requires__ = 'chimera-python==0.2.dev-r415'<br>
import pkg_resources<br>
pkg_resources.run_script('chimera-python==0.2.dev-r415', 'chimera')<br>
</code></pre>
</td>

<a href='Hidden comment: ============ explanation ============'></a><br>
<br>
<td valign='top'> This is the "binary" package which calls<br>
<ul>
<li> <b><code>/usr/lib/python2.5/site-packages/pkg_resources.py</code></b> which looks into the </li>
<li> <b><code>/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/</code></b> and into its </li>
<li> <b><code>EGG-INFO/scripts</code></b> folder and runs the </li>
<li> <b><code>chimera</code></b> script </li>
</ul>
</td>
</tr>





<a href='Hidden comment:  ************************* table row ************************'></a><br>
<tr>

<a href='Hidden comment: ============ call ============'></a><br>
<br>
<td valign='top'><code>/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/EGG-INFO/scripts/chimera</code> </td>

<a href='Hidden comment: ============ snippit ============'></a><br>
<br>
<td valign='top'>
<pre><code>#!/usr/bin/python<br>
def main ():<br>
<br>
import sys<br>
<br>
from chimera.controllers.site.main import SiteController<br>
<br>
SiteController(sys.argv).startup()<br>
<br>
<br>
if __name__ == '__main__':<br>
main()<br>
</code></pre>
</td>

<a href='Hidden comment: ============ explanation ============'></a><br>
<br>
<td valign='top'> The 'chimera' script defines a <b><code>main</code></b> method and calls that main method. <br />
This main method calls <b><code>chimera.controllers.site.main</code></b> which is the file main.py.<br />
This file defines the class <b><code>SiteController</code></b>.<br />
It imports the <b><code>SiteController</code></b> class and calls <b><code>SiteController(sys.argv).startup()</code></b> on that class. </td>
</tr>




<a href='Hidden comment:  ************************* table row ************************'></a><br>
<tr>

<a href='Hidden comment: ============ call ============'></a><br>
<br>
<td valign='top'><code>/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/controllers/site/main.py</code></td>

<a href='Hidden comment: ============ snippit ============'></a><br>
<br>
<td valign='top'>
<pre><code>def startup(self):<br>
<br>
if self.options.daemon:<br>
# detach<br>
log.info("FIXME: Daemon...")<br>
<br>
# system config<br>
self.config = SystemConfig.fromFile(self.options.config_file, self.options.use_global)<br>
<br>
# manager<br>
if not self.options.dry:<br>
log.info("Starting system.")<br>
log.info("Chimera version: %s" % find_dev_version() or _chimera_version_)<br>
log.info("Chimera prefix: %s" % ChimeraPath.root())<br>
<br>
try:<br>
self.manager = Manager(**self.config.chimera)<br>
except ChimeraException, e:<br>
log.error("Chimera is already running on this machine. Use chimera-admin to manage it.")<br>
sys.exit(1)<br>
<br>
log.info("Chimera: running on "+ self.manager.getHostname() + ":" + str(self.manager.getPort()))<br>
if self.options.use_global:<br>
log.info("Chimera: reading configuration from %s" % SYSTEM_CONFIG_DEFAULT_GLOBAL)<br>
log.info("Chimera: reading configuration from %s" % os.path.realpath(self.options.config_file))<br>
<br>
# add site object<br>
if not self.options.dry:<br>
<br>
for site in self.config.sites:<br>
self.manager.addClass(Site, site.name, site.config, True)<br>
<br>
# search paths<br>
log.info("Setting objects include path from command line parameters...")<br>
for _dir in self.options.inst_dir:<br>
self.paths["instruments"].append(_dir)<br>
<br>
for _dir in self.options.ctrl_dir:<br>
self.paths["controllers"].append(_dir)<br>
<br>
for _dir in self.options.drv_dir:<br>
self.paths["drivers"].append(_dir)<br>
<br>
# init from config<br>
log.info("Trying to start drivers...")<br>
for drv in self.config.drivers + self.options.drivers:<br>
<br>
if self.options.dry:<br>
print drv<br>
else:<br>
self._add(drv, path=self.paths["drivers"], start=True)<br>
<br>
log.info("Trying to start instruments...")<br>
for inst in self.config.instruments + self.options.instruments:<br>
<br>
if self.options.dry:<br>
print inst<br>
else:<br>
self._add(inst, path=self.paths["instruments"], start=True)<br>
<br>
log.info("Trying to start controllers...")<br>
for ctrl in self.config.controllers + self.options.controllers:<br>
<br>
if self.options.dry:<br>
print ctrl<br>
else:<br>
self._add(ctrl, path=self.paths["controllers"], start=True)<br>
<br>
log.info("System up and running.")<br>
<br>
# ok, let's wait manager work<br>
if self.wait and not self.options.dry:<br>
self.manager.wait()<br>
<br>
</code></pre>
</td>

<a href='Hidden comment: ============ explanation ============'></a><br>
<br>
<td valign='top'>
This is the method startup() which is inside the SiteController class.<br />
This method calls <code>Manager(**self.config.chimera)</code> which instantiates a Manger object.<br />
The manager object is then used to obtain all the resources for the chimera program.<br />
Note: you can see the <code>log.info()</code> method is the stuff printed when starting chimera. For example, you will see that <code>log.info("Starting system.")</code> is what is printed to the server's terminal window upon startup.<br>
</td>
</tr>



<a href='Hidden comment:  ************************* table row ************************'></a><br>
<tr>

<a href='Hidden comment: ============ call ============'></a><br>
<br>
<td valign='top'><code>/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/core/manager.py</code></td>

<a href='Hidden comment: ============ snippit ============'></a><br>
<br>
<td valign='top'>
<pre><code><br>
<br>
class Manager (RemoteObject):<br>
<br>
"""<br>
This is the main class of Chimera.<br>
<br>
Use this class to get Proxies, add objects to the system, and so on.<br>
<br>
This class handles objects life-cycle as described in ILifecycle.<br>
<br>
@group Add/Remove: add*, remove<br>
@group Start/Stop: start, stop<br>
@group Proxy: getProxy<br>
@group Shutdown: wait, shutdown<br>
<br>
"""<br>
<br>
def __init__(self, host = None, port = None, local=False):<br>
RemoteObject.__init__ (self)<br>
<br>
log.info("Starting manager.")<br>
<br>
self.resources = ResourcesManager()<br>
self.classLoader = ClassLoader()<br>
<br>
# identity<br>
self.setGUID(MANAGER_LOCATION)<br>
<br>
# shutdown event<br>
self.died = threading.Event()<br>
<br>
if not local:<br>
    try:<br>
        ManagerLocator.locate()<br>
        raise ChimeraException("Chimera is already running"<br>
                               " on this system. Use chimera-admin"<br>
                               " to manage it.")<br>
    except ManagerNotFoundException:<br>
        # ok, we are alone.<br>
        pass<br>
<br>
# our daemon server<br>
self.adapter = ManagerAdapter (self, host, port)<br>
self.adapterThread = threading.Thread(target=self.adapter.requestLoop)<br>
self.adapterThread.setDaemon(True)<br>
self.adapterThread.start()<br>
<br>
# finder beacon<br>
if not local:<br>
    self.beacon = ManagerBeacon(self)<br>
    self.beaconThread = threading.Thread(target=self.beacon.run)<br>
    self.beaconThread.setDaemon(True)<br>
    self.beaconThread.start()<br>
else:<br>
    self.beacon = None<br>
<br>
# register ourself<br>
self.resources.add(MANAGER_LOCATION, self, getManagerURI(self.getHostname(), self.getPort()))<br>
<br>
# signals<br>
signal.signal(signal.SIGTERM, self._sighandler)<br>
signal.signal(signal.SIGINT, self._sighandler)<br>
atexit.register (self._sighandler)<br>
<br>
<br>
</code></pre>
</td>

<a href='Hidden comment: ============ explanation ============'></a><br>
<br>
<td valign='top'>The file <b><code>manager.py</code></b> contains multiple classes.<br />
It contains <code>Manager</code> and <code>ManagerAdapter</code>.<br />
This snippet is where the constructor for the class <code>Manager</code> is called which in turn creates a <code>MangerAdapter</code> (see after the comment  <code># our daemon server</code>).<br />
Also note the comment,<br>
<pre><code> """<br>
This is the main class of Chimera.<br>
Use this class to get Proxies, <br>
add objects to the system, and so on.<br>
This class handles objects life-cycle<br>
 as described in ILifecycle.<br>
"""<br>
</code></pre>
<b>Eurika!!!</b>
</td>
</tr>




<a href='Hidden comment:  ************************* table row ************************'></a><br>
<br>
<br>
<tr>

<a href='Hidden comment: ============ call ============'></a><br>
<br>
<td valign='top'><code>/usr/lib/python2.5/site-packages/chimera_python-0.2.dev_r415-py2.5.egg/chimera/core/manager.py</code></td>

<a href='Hidden comment: ============ snippit ============'></a><br>
<br>
<td valign='top'>
<pre><code>class ManagerAdapter (Pyro.core.Daemon):<br>
<br>
    def __init__ (self, manager, host = None, port = None):<br>
<br>
        Pyro.core.initServer(banner=False)<br>
        <br>
        Pyro.core.Daemon.__init__ (self,<br>
                                   host=host or MANAGER_DEFAULT_HOST,<br>
                                   port=port or MANAGER_DEFAULT_PORT,<br>
                                   norange=0)<br>
<br>
        self.useNameServer(None)<br>
        self.connect (manager)<br>
<br>
        # saved here to give objects a manager when they ask<br>
        self.manager = manager<br>
<br>
        self.getAdapter().setTimeout(None)<br>
<br>
    def getManager (self):<br>
        return self.manager<br>
<br>
    def getProxyForObj(self, obj):<br>
        return Proxy(uri=Pyro.core.PyroURI(self.hostname,<br>
                                           obj.GUID(), prtcol=self.protocol, port=self.port))<br>
<br>
    def connect(self, obj, name=None, index=None):<br>
<br>
        URI = Pyro.core.PyroURI(self.hostname, obj.GUID(), prtcol=self.protocol, port=self.port)<br>
<br>
        self.implementations[obj.GUID()] = (obj, name)            <br>
        <br>
        if index:<br>
            self.implementations[index] = (obj, name)<br>
<br>
        obj.setPyroDaemon(self)<br>
<br>
        return URI<br>
<br>
<br>
</code></pre>
</td>

<a href='Hidden comment: ============ explanation ============'></a><br>
<br>
<td valign='top'>The file <b><code>manager.py</code></b> contains multiple classes.<br />
It contains <code>Manager</code> and <code>ManagerAdapter</code>.<br />
Here is the class definition for <code>ManagerAdapter</code>, which calls on the Pyro package to initialize a server.<br />
Note: This seems to act like a singleton class which returns the server if it is already created.<br>
This pyro package is dependent upon /usr/lib/python2.5/site-packages/Pyro-3.8.1-py2.5.egg/Pyro/configuration.py<br>
</td>
</tr>


</tbody>
</table>