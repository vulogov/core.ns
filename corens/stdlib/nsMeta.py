from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsMetaInit(ns, *args, **kw):
    if len(nsDir(ns, "/etc/meta")) == 0:
        return
    print(nsDir(ns, "/etc/meta"))
    nsconsole(ns, "Metaprogramming start")

def nsMetaStop(ns, *args, **kw):
    if len(nsDir(ns, "/etc/meta")) == 0:
        return
    nsconsole(ns, "Metaprogrammming stop")

_init = [
    "metaprogramming"
]

_actions = {
    "metaprogramming": {
        "start" : nsMetaInit,
        "stop" : nsMetaStop
    }
}
