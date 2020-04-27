from corens.console import nsconsole
from corens.log import *
from corens.ns import *
from corens.zmq import *

def nsBlocksInit(ns, *args, **kw):
    if len(nsDir(ns, "/usr/local/blocks/")) > 0:
        nsInfo(ns, "Creating application BLOCKS")
        for b in nsDir(ns, "/usr/local/blocks/"):
            f = nsGet(ns, "/usr/local/blocks/{}/init".format(b))
            if f is None:
                continue
            nsInfo(ns, "Application BLOCK: {} initializing".format(b))
            if f() is True:
                nsInfo(ns, "Application BLOCK: {} OK".format(b))
            else:
                nsError(ns, "Application BLOCK: {} FAILED".format(b))

def nsBlocksStop(ns, *args, **kw):
    nsInfo(ns, "Removing application BLOCKS")

_init = [
    "z97_blocks"
]

_actions = {
    "z97_blocks": {
        "start" : nsBlocksInit,
        "stop" : nsBlocksStop
    }
}
