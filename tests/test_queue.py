import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_queue_1():
    ns, f, F = NS()
    f("/dev/queue/open")("test")
    f("/dev/q/test/put")(42)
    assert f("/dev/q/test/get")() == 42
