import sys
import os
import time
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *
import gevent
from corens.mod import lf
from corens.console import nsConsole, nsconsole

def send_event(ns):
    f = lf(ns)
    nsconsole(ns, "SEND: {}".format(f("/tasks/gate/test/in")(random.randint(1,100))))

def recv_event(ns):
    nsconsole(ns, "RECV: {}".format(f("/tasks/gate/test/empty")()))

def closeopen(ns):
    state = f("/tasks/gate/test/trigger")()
    print("TRIGGER from ",state)
    gevent.sleep(8)
    state = f("/tasks/gate/test/trigger")()
    print("TRIGGER from ",state)



ns, f, F = NS()
f("/blocks/gate/create")("test", blocking=True)
f("schedule")(1, "EVENTSENDER", send_event)
f("schedule")(1, "EVENTRECV", recv_event)
f("schedule")(10, "TRIGGER", closeopen)
f("/sbin/loop")()
