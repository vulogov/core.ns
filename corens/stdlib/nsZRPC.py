from corens.console import nsconsole
from corens.ns import *


def nsZRpcInit(ns, *args, **kw):
    nsconsole(ns, "ZRPC start")

def nsZRpcStop(ns, *args, **kw):
    nsconsole(ns, "ZRPC stop")

_init = [
    "zrpc"
]

_actions = {
    "zrpc": {
        "start" : nsZRpcInit,
        "stop" : nsZRpcStop
    }
}
