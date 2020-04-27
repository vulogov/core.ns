from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsPipelinesInit(ns, *args, **kw):
    nsconsole(ns, "PIPELINES start")

def nsPipelinesStop(ns, *args, **kw):
    nsconsole(ns, "PIPELINES stop")

_init = [
    "z99_pipelines"
]

_actions = {
    "z99_pipelines": {
        "start" : nsPipelinesInit,
        "stop" : nsPipelinesStop
    }
}
