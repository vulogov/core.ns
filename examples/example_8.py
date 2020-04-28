import sys
import os
import time
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *
from corens.mod import lf
from corens.console import nsConsole, nsconsole


def recv_event(ns):
    nsConsole(ns, "RECV: {}".format(f("/tasks/emit/test/empty")()))

def handler(ns, block_path, task_path, data, *args, **kw):
    n = random.randint(1,100)
    print("GENERATE:", n)
    return n


ns, f, F = NS()
f("/blocks/emit/create")("test", f("p")(handler), blocking=True, sleep=1)
f("schedule")(5, "EVENTRECV", recv_event)
f("/sbin/loop")()
