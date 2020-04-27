import sys
import os
import time
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *
from corens.mod import lf
from corens.console import nsConsole, nsconsole

def send_event(ns):
    f = lf(ns)
    nsConsole(ns, "SEND: {}".format(f("/tasks/tee/test/in")(random.randint(1,100))))

def recv_event(ns):
    f = lf(ns)
    nsConsole(ns, "RECV: {}".format(f("/tasks/tee/test/out")()))

def monitor_event(ns):
    f = lf(ns)
    nsConsole(ns, "MONITOR: {}".format(f("/tasks/tee/test/monitor")()))

ns, f, F = NS()
f("/blocks/tee/create")("test", blocking=True)
f("schedule")(1, "EVENTSENDER", send_event)
f("schedule")(1, "EVENTRECV", recv_event)
f("schedule")(1, "EVENTMONITOR", monitor_event)
f("/sbin/loop")()
