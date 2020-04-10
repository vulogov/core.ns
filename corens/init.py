import re
import sys
import atexit
from corens.ns import *
from corens.tpl import *
from corens.mod import f
from corens.hylang import nsHyEval, nsHyPipeline

def matchInitName(name):
    r = re.match(r'(\d+)\_([a-zA-Z]+)', name)
    if r is None:
        return False
    if r.span()[0] == 0 and r.span()[1] == len(name):
        return True
    return False

def nsInitExecute(ns, action, *args, **kw):
    initd = nsLs(ns, "/etc/init.d")
    _cmds = list(initd.keys())
    _cmds.sort()
    if re.match("^stop(.\w*)*", action) is not None:
        _cmds.reverse()
    for i in _cmds:
        fun = f(ns, "/etc/init.d/{}/{}".format(i, action))
        if fun is None:
            continue
        fun(*args, **kw)
        fun = f(ns, "V")("/etc/init.d/{}/{}Hy".format(i, action))
        if fun is not None:
            nsHyEval(ns, fun)
        fun = f(ns, "V")("/etc/init.d/{}/{}Pipe".format(i, action))
        if fun is not None:
            nsHyPipeline(ns, fun)

def nsInit(ns, *args, **kw):
    tpls = nsLs(ns, "/templates")
    for i in tpls:
        if matchInitName(i) is True:
            nsMk(ns, i, *args, **kw)
    nsInitExecute(ns, "start", *args, **kw)
    atexit.register(nsStop, ns)
    return True

def nsStop(ns):
    nsInitExecute(ns, "stop", *(), **{})
    return True

def nsInitMk(ns, name, start, stop, **kw):
    if name in nsLs(ns, "/etc/init.d"):
        return
    path = "/etc/init.d/{}".format(name)
    nsMkdir(ns, path)


def nsDummyMain(ns, *args, **kw):
    return ns
