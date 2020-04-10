import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

from corens import *

def test_args_1():
    ns, f, F = NS(args=['a','b','--m', '--f', '42'])
    V = f("V")
    assert V('/etc/args/a/__name__') == '/etc/args/a'

def test_args_2():
    ns, f, F = NS(args=['a','b','--m', '--f', '42'])
    V = f("V")
    assert len(V('/etc/argv')) == 2

def test_args_3():
    ns, f, F = NS(args=['a','b','--m', '--f', '42'])
    V = f("V")
    assert V('/etc/args/b/m') == True

def test_args_4():
    ns, f, F = NS(args=['a','b','--m', '--f', '42'])
    V = f("V")
    assert V('/etc/args/b/f') == '42'

def test_args_5():
    ns, f, F = NS(args=['+flag'])
    V = f("V")
    assert V('/etc/flags/flag') == True

def test_args_6():
    ns, f, F = NS(args=['-flag'])
    V = f("V")
    assert V('/etc/flags/flag') == False
