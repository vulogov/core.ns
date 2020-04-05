import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def answer(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    V("/tmp/answer", 42)

def test_gevt_1():
    ns, f, F = NS()
    V = f("V")
    f("spawn")("answer", answer)
    f("/bin/loop")()
    assert V("/tmp/answer") == 42
