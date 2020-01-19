import gevent
import time
from apscheduler.schedulers.gevent import GeventScheduler
from corens.ns import *
from corens.tpl import nsMk

def nsGevent(ns):
    nsMkdir(ns, "/proc")
    nsSet(ns, "/sys/greenlets", [])
    nsSet(ns, "/sys/scheduler", GeventScheduler())
    s = nsGet(ns, "/sys/scheduler")
    g = s.start()
    ns = nsProcAlloc(ns, "scheduler", g, scheduler=s)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    nsMk(ns, "queue")
    return ns

def nsProcAlloc(ns, name, g, **kw):
    path = "/proc/{}".format(name)
    nsMkdir(ns, path)
    for k in kw:
        nsSet(ns, "{}/{}".format(path, k), kw[k])
    nsSet(ns, "{}/proc".format(path), g)
    nsSet(ns, "{}/stamp".format(path), time.time())
    return ns

def nsSpawn(ns, name, fun, *args, **kw):
    _args = tuple([ns,] + list(args))
    g = gevent.Greenlet(fun, args, kw)
    g.name = name
    nsProcAlloc(ns, name, g)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    g.start()
    return ns
