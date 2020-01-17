import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_dev_1():
    ns, f, F = NS()
    V = f("V")
    Mk = f("Mk")
    Mk("time")
    assert type(V("/dev/time/read")()) == type(0.0)
