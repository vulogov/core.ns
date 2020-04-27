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
    nsConsole(ns, "SEND: {}".format(f("/tasks/pass/test/in")(random.randint(1,100))))

def recv_event(ns):
    nsConsole(ns, "RECV: {}".format(f("/tasks/pass/test/out")()))

def add1(ns, block_path, task_path, data, *args, **kw):
    print("TADA", data)
    return data+1


ns, f, F = NS()
f("/blocks/pass/create")("test", f("p")(add1), blocking=True)
f("schedule")(1, "EVENTSENDER", send_event)
f("schedule")(1, "EVENTRECV", recv_event)
f("/sbin/loop")()
