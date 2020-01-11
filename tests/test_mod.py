import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_mod_1():
    ns, f, F = NS()
    assert type(f("stamp")()) == type(0.0)

def test_mod_2():
    ns, f, F = NS()
    F("stamp")
    assert type(stamp()) == type(0.0)
