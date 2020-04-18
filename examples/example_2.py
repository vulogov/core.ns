import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *

ns, f, F = NS()
V = f("V")
print(V("/etc/argv"))
print("Me application name as passed by user", V("/etc/args/default/appname"))
print("Me application name as detected", V("/etc/name"))
print("Me configurations", V("/etc/args/default/conf"))
print("Me name", V("/etc/name"))
print("Me flags", V("/etc/flags"))
print("Config files", V("/config/cfg.files"))
print("Proof that test_example.cfg is loaded", V("/home/trueAndOnlyAnswer"))
print("Hostname", V("/etc/hostname"))
print("Listen", V("/etc/listen"))
