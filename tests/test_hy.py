import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_hy_1():
    ns, f, F = NS()
    V = f("V")
    assert V("/sys/hylang.enabled") == True

def test_hy_2():
    ns, f, F = NS()
    hy = f("hy")
    assert hy("(+ 41 1)") == 42

def test_hy_3():
    ns, f, F = NS()
    assert f("h|")("1 (+ 41)") == 42

def test_hy_4():
    ns, f, F = NS()
    f("/dev/q/hy/put")(42)
    assert f("/dev/q/hy/get")() == 42
