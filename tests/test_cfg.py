import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_cfg_0():
    ns, f, F = NS()
    V = f("V")
    Cfg = f("Cfg")
    Cfg("test.cfg")
    assert V('/home/NotAnswer') == 41


def test_cfg_1():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('("test.cfg" >')
    assert V('/home/NotAnswer') == 41

def test_cfg_2():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('[ /home > ;;' )

def test_cfg_3():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('[ /home > Answer <- 42 ;;' )
    assert V('/home/Answer') == 42

def test_cfg_4():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('[ /home > Pi <- 3.14 ;;' )
    assert V('/home/Pi') == 3.14

def test_cfg_5():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('[ /home > Message <- "Hello World!" ;;' )
    assert V('/home/Message') == "Hello World!"

def test_cfg_6():
    ns, f, F = NS()
    V = f("V")
    C = f("C")
    C('[ /home > [1, 3.14, "Hello"] -> List ;;' )
    assert len(V('/home/List')) == 3
