from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsZMQInit(ns, *args, **kw):
    if len(nsGet(ns, "/etc/zmq")) == 0:
        return
    nsconsole(ns, "ZMQ start")

def nsZMQStop(ns, *args, **kw):
    if len(nsGet(ns, "/etc/zmq")) == 0:
        return
    nsconsole(ns, "ZMQ stop")

_init = [
    "zmq"
]

_actions = {
    "zmq": {
        "start" : nsZMQInit,
        "stop" : nsZMQStop
    }
}
