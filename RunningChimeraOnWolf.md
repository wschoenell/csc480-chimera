# Introduction #

These are the steps you need to take in order for you run Chimera on Wolf.

# Details #

For Wolf, substitude "/usr/lib/python2.5/site-packages/chimera\_python-0.2.dev\_r415-py2.5.egg/chimera/core/c" for {PYTHON} in directory locations.

  * Create an empty text file called "chimera.config" in your "~/.chimera/" directory. The reason for this is because Chimera looks for a file called "chimera.sample.config" in "{PYTHON}/chimera/core/". When it's not found, it then defaults to your "chimera.config". I attempted to put the contents of "chimera/core/chimera.global.config" in it, but another error is thrown, telling me the content was already loaded elsewhere. I'm not sure where that's happening yet. This seems to get Chimera working.

  * Steps to reproduce:
    1. Log into wolf
      * If you're already logged into moxie, just type: `ssh wolf`
      * If you're not, log into moxie: `ssh {username}@moxie.oswego.edu` and then log into wolf.
    1. Create the config file: `touch ~/.chimera/chimera.config`
    1. Run Chimera: `chimera -vv`

  * This is definitely a quick fix. If the config information is already loaded, then it does not need to look in `~/.chimera/chimera.config`. Feel free to add any information about this. (If you're too scared to modify code, post what needs to be done.)