import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_version_1():
    ns, f, F = NS()
    V = f("V")
    assert V("/etc/corens/license") == 'GPL3'
