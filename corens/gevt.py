import gevent
import sys
import time
from apscheduler.schedulers.gevent import GeventScheduler
from corens.ns import *
from corens.mod import f
from corens.tpl import nsMk

def nsGInput(ns):
    prompt = nsGet(ns, "/etc/shell.prompt")
    sys.stdout.write(prompt)
    sys.stdout.flush()
    gevent.select.select([sys.stdin], [], [])
    return sys.stdin.readline().strip()



def nsGevent(ns, *args, **kw):
    nsMkdir(ns, "/proc")
    nsSet(ns, "/sys/greenlets", [])
    nsSet(ns, "/sys/scheduler", GeventScheduler())
    s = nsGet(ns, "/sys/scheduler")
    g = s.start()
    ns = nsProcAlloc(ns, "scheduler", g, scheduler=s)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    nsMk(ns, "queue")
    f(ns, "/dev/queue/open")("shell")
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

def nsKillAll(ns):
    return ns
