from corens.console import nsconsole
from corens.ns import *


def nsRpcInit(ns, *args, **kw):
    nsconsole(ns, "RPC start")

def nsRpcStop(ns, *args, **kw):
    nsconsole(ns, "RPC stop")

def nsInternalServerStart(ns, *args, **kw):
    nsconsole(ns, "INTERNAL RPC start")
    if nsGet(ns, "/etc/flags/internalServer", False) is True:
        nsconsole(ns, "Internal RPC server enabled")
    else:
        nsconsole(ns, "Internal RPC server disabled")

def nsInternalServerStop(ns, *args, **kw):
    nsconsole(ns, "INTERNAL RPC stop")

_init = [
    "rpc", "internal"
]

_actions = {
    "rpc": {
        "start" : nsRpcInit,
        "stop" : nsRpcStop
    },
    "internal": {
        "start": nsInternalServerStart,
        "stop": nsInternalServerStop
    }
}
