import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens.ns import *

def test_ns_1():
    d = NS()
    assert(type(d) == dict)

def test_ns_2():
    ns = NS()
    l1 = nsGet(ns, "/sys/log/messages", None)
    assert l1.qsize() == 0
