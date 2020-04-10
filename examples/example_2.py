from corens import *

ns, f, F = NS()
V = f("V")
print(V("/etc/argv"))
print(V("/etc/args/default/appname"))
print(V("/etc/name"))
print(V("/config/cfg.path"))
print(V("/etc/flags"))

