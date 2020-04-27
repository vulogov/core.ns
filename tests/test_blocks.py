import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_blocks_1():
    ns, f, F = NS()
    assert f("/blocks/echo/create")("test")

def test_blocks_2():
    ns, f, F = NS()
    f("/blocks/echo/create")("test")
    assert f("/tasks/echo/test/in")(42) == True

def test_blocks_3():
    ns, f, F = NS()
    f("/blocks/echo/create")("test")
    f("/tasks/echo/test/in")(42)
    assert f("/tasks/echo/test/out")() == 42
