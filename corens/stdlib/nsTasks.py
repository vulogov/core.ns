from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsTasksInit(ns, *args, **kw):
    nsconsole(ns, "TASKS start")

def nsTasksStop(ns, *args, **kw):
    nsconsole(ns, "TASKS stop")

_init = [
    "z98_tasks"
]

_actions = {
    "z98_tasks": {
        "start" : nsTasksInit,
        "stop" : nsTasksStop
    }
}
