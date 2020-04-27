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
    nsConsole(ns, "SEND: {}".format(f("/tasks/filter/test/in")(random.randint(1,100))))

def recv_event(ns):
    nsConsole(ns, "RECV: {}".format(f("/tasks/filter/test/out")()))

def print_rejection(ns, block_path, task_path, data):
    print("REJECTED:", data)
    return data

ns, f, F = NS()
f("/blocks/filter/create")("test", f("p")(lambda ns,a,b,x: x < 50), f("p")(print_rejection), blocking=True)
f("schedule")(1, "EVENTSENDER", send_event)
f("schedule")(2, "EVENTRECV", recv_event)
f("/sbin/loop")()
