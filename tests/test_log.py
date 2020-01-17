import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens.ns import *
from corens.log import *

def test_log_1():
    ns = NS()
    nsInfo(ns, "test")
    assert nsLogSize(ns) == 1

def test_log_2():
    ns = NS()
    nsInfo(ns, "test")
    nsLogProcess(ns)
    assert nsLogSize(ns) == 0
