import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def answer(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    V("/tmp/answer", 42)

def killer(ns):
    f = lf(ns)
    while True:
        V = f("V")
        V("/tmp/answer", 42)
        time.sleep(1)
        f("/sbin/killall")()

def killer5(*args):
    f = lf(args[0])
    c = 0
    while True:
        c += 1
        time.sleep(1)
        if c > 5:
            break
    f("/sbin/killall")()

def test_gevt_1():
    ns, f, F = NS()
    V = f("V")
    f("spawn")("answer", answer)
    f("/bin/loop")()
    assert V("/tmp/answer") == 42

def test_gevt_2():
    ns, f, F = NS()
    V = f("V")
    f("spawn")("killer", killer)
    f("/bin/loop")()
    assert V("/tmp/answer") == 42

def test_gevt_3():
    ns, f, F = NS()
    V = f("V")
    f("schedule")(1, "42", answer)
    f("spawn")("killer", killer5)
    f("/sbin/loop")()
    assert V("/tmp/answer") == 42
