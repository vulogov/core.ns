import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_mod_1():
    ns, f, F = NS()
    assert type(f("stamp")()) == type(0.0)

def test_mod_2():
    ns, f, F = NS()
    F("stamp")
    assert type(stamp()) == type(0.0)

def test_mod_3():
    ns, f, F = NS()
    V = f("V")
    assert V("/config/answer") == 42

def test_mod_4():
    ns, f, F = NS()
    V = f("V")
    assert V("/config/answer", 43) == 43

def test_mod_5():
    ns, f, F = NS()
    V = f("V")
    V("/config/var.redefine", False)
    assert V("/config/answer", 43) == 42

def test_mod_6():
    ns, f, F = NS()
    Random = f("random")
    assert len(Random()) == 1
