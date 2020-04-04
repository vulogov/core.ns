import os
import platform
import getpass
import shutil
from pathlib import Path
from corens.ns import nsSet, nsGet, nsMkdir

def nsEnvVars(ns):
    for e in os.environ:
        nsSet(ns, "/sys/env/variables/{}".format(e), os.environ[e])

def nsEnvInit(ns, *args, **kw):
    nsMkdir(ns, "/sys/env")
    nsMkdir(ns, "/sys/env/variables")
    nsMkdir(ns, "/sys/env/platform")
    nsEnvVars(ns)
    nsSet(ns, "/sys/env/platform/architecture", platform.architecture()[0])
    nsSet(ns, "/sys/env/platform/machine", platform.machine())
    nsSet(ns, "/sys/env/platform/node", platform.node())
    nsSet(ns, "/sys/env/platform/platform", platform.platform())
    nsSet(ns, "/sys/env/platform/python", platform.python_version().split('.'))
    nsSet(ns, "/sys/env/platform/system", platform.system())
    nsSet(ns, "/sys/env/platform/uname", platform.uname())
    nsSet(ns, "/sys/env/uid", os.getuid())
    nsSet(ns, "/sys/env/user", getpass.getuser())
    nsSet(ns, "/sys/env/home", str(Path.home()))
    home_total, home_used, home_free = shutil.disk_usage(nsGet(ns, "/sys/env/home"))
    nsSet(ns, "/sys/env/home.disk.size", home_total)
    nsSet(ns, "/sys/env/home.disk.used", home_used)
    nsSet(ns, "/sys/env/home.disk.free", home_free)
    nsSet(ns, "/sys/env/home.disk.free.percent", (home_free/home_total)*100)
    
