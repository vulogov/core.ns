import os
import os.path
import platform
import getpass
import shutil
import stat
import fnmatch
import socket
import atexit
import time
import psutil
import uuid
from pathlib import Path
from corens.ns import nsSet, nsGet, nsMkdir, nsGlobalError, nsLs
from corens.mod import I, lf
from corens.cfg_grammar import nsCfgLoad, nsCfgFSLoad
from corens.cfg import nsCfgAppendFs
from corens.console import nsConsole, nsconsole
from corens.gevt import nsSchedulerIntervalJob

def nsEnvVars(ns):
    for e in os.environ:
        nsSet(ns, "/sys/env/variables/{}".format(e), os.environ[e])

def check_the_path(ns, path):
    if not os.path.exists(path) and not os.path.isdir(path):
        return False
    _stat = os.stat(path)
    if _stat.st_uid != nsGet(ns, "/sys/env/uid"):
        return False
    if stat.S_IMODE(os.lstat(path).st_mode) != 448:
        return False
    return True

def nsEnvRemovePid(ns):
    daemonFile = "{}.daemon".format(nsGet(ns, "/sys/env/pidFile"))
    if os.path.exists(daemonFile) and os.path.isfile(daemonFile):
        return
    f = lf(ns)
    V = f("V")
    if nsGet(ns, "/etc/daemonize") is True:
        return
    nsconsole(ns, "Removing PID file")
    if os.path.exists(nsGet(ns, "/sys/env/pidFile")) and os.path.isfile(nsGet(ns, "/sys/env/pidFile")):
        os.remove(nsGet(ns, "/sys/env/pidFile"))

def nsEnvRemovePidSignal(ns, sig, frame):
    nsEnvRemovePid(ns)

def nsEnvLoadLocalBS(ns):
    CNS_HOME = nsGet(ns, "/sys/env/variables/CORENS_HOME")
    CNS_NAME = nsGet(ns, "/sys/env/variables/CORENS_NAME")
    if CNS_NAME is None:
        CNS_NAME = nsGet(ns, "/etc/name")
    if CNS_HOME is None:
        _path = ["{}/.{}".format(nsGet(ns, "/sys/env/cwd"),nsGet(ns,"/etc/name")),
                "{}/.{}".format(nsGet(ns, "/sys/env/home"),nsGet(ns,"/etc/name"))
        ]
        for p in _path:
            if check_the_path(ns, p) is True:
                CNS_HOME = p
                break
        if CNS_HOME is None:
            CNS_HOME = "{}/.{}".format(nsGet(ns, "/sys/env/home"),nsGet(ns,"/etc/name"))
            os.mkdir(CNS_HOME)
            os.chmod(CNS_HOME, 0o700)
    nsSet(ns, "/sys/env/apphome", CNS_HOME)
    cfg_path = nsGet(ns, "/config/cfg.path")
    cfg_path.append("osfs://{}".format(CNS_HOME))
    if check_the_path(ns, "/etc/{}".format(CNS_NAME)) is True:
        cfg_path.append("osfs:///etc/{}".format(CNS_NAME))
    nsSet(ns, "/config/cfg.path", cfg_path)
    nsSet(ns, "/sys/env/pidFile", "{}/{}.pid".format(CNS_HOME, CNS_NAME))
    pidExists = False
    if os.path.exists(nsGet(ns, "/sys/env/pidFile")) and os.path.isfile(nsGet(ns, "/sys/env/pidFile")):
        pidExists = True
    if nsGet(ns, "/etc/singleCopy") is True and pidExists is True:
        nsConsole(ns, "Application $etc.name already running")
        nsGlobalError(ns, "Application {} already running.".format(CNS_NAME))
        raise SystemExit
    nsSet(ns, "/sys/env/pidFileExists", pidExists)
    if nsGet(ns, "/etc/flags/daemonize", False):
        nsEnvMkPID(ns)
    for p in cfg_path:
        nsCfgAppendFs(ns, p)


def nsEnvMkPID(ns):
    if nsEnvLoadPid(ns) is not None:
        return
    with open(nsGet(ns, "/sys/env/pidFile"), "w") as f:
        f.write(str(os.getpid()))

def nsEnvLoadPid(ns):
    try:
        with open(nsGet(ns, "/sys/env/pidFile"), "r") as f:
            try:
                pid = int(f.read())
            except ValueError:
                return None
    except FileNotFoundError:
        return None
    try:
        me = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return None
    if me.is_running() is True:
        return pid
    return None

def nsProcTick(ns):
    p = psutil.Process()
    with p.oneshot():
        nsSet(ns, "/sys/env/proc/name", p.name())
        nsSet(ns, "/sys/env/proc/cpuTimes", p.cpu_times())
        nsSet(ns, "/sys/env/proc/cpuPercent", p.cpu_percent())
        nsSet(ns, "/sys/env/proc/createTime", p.create_time())

def nsEnvInit(ns, *args, **kw):
    f = lf(ns)
    nsMkdir(ns, "/sys/env")
    nsSet(ns, "/sys/env/id", str(uuid.uuid4()))
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
    nsSet(ns, "/sys/env/cwd", os.getcwd())
    home_total, home_used, home_free = shutil.disk_usage(nsGet(ns, "/sys/env/home"))
    nsSet(ns, "/sys/env/home.disk.size", home_total)
    nsSet(ns, "/sys/env/home.disk.used", home_used)
    nsSet(ns, "/sys/env/home.disk.free", home_free)
    nsSet(ns, "/sys/env/home.disk.free.percent", (home_free/home_total)*100)
    nsSet(ns, "/sys/env/bootTimestamp", time.time())
    nsSet(ns, "/sys/env/pid", os.getpid())
    nsSet(ns, "/sys/env/me", psutil.Process(os.getpid()))
    nsMkdir(ns, "/sys/env/proc")
    try:
        nsSet(ns, "/sys/env/ip.addr", socket.gethostbyname(socket.gethostname()))
        nsSet(ns, "/sys/env/ip.addr.list", socket.gethostbyname_ex(socket.gethostname())[2])
    except socket.gaierror:
        nsSet(ns, "/sys/env/ip.addr", '127.0.0.1')
        nsSet(ns, "/sys/env/ip.addr.list", ['127.0.0.1'])
    if nsGet(ns, "/etc/flags/truename", False) is True:
        nsSet(ns, "/etc/hostname", nsGet(ns, "/sys/env/platform/node"))
    nsEnvLoadLocalBS(ns)
    for k in kw:
        _k = "/"+k[4:].replace("_", "/")
        if fnmatch.fnmatch(k, "__V_*") is True:
            _k = "/"+k[4:].replace("_", "/")
            nsSet(ns, _k, kw[k])
        if k[0] == "/":
            nsSet(ns, k, kw[k])
        elif fnmatch.fnmatch(k, "__F_*") is True:
            dir = os.path.dirname(_k)
            nsMkdir(ns, dir)
            I(ns, _k, kw[k])
        elif fnmatch.fnmatch(k, "__C_*") is True:
            nsCfgLoad(ns, kw[k])
        elif fnmatch.fnmatch(k, "__B_*") is True:
            nsCfgFSLoad(ns, kw[k])
        else:
            pass

def nsEnvSetup(ns):
    nsSchedulerIntervalJob(ns, 60, "/dev/proc", nsProcTick)
    for f in nsLs(ns, "/bin/atexit"):
        atexit.register(nsGet(ns, "/bin/atexit/{}".format(f)))
