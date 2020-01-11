import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_mod_1():
    ns, F = NS()
    assert type(F("stamp")()) == type(0.0)
