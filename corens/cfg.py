from corens.ns import *

def nsDefaults(ns):
    nsSet(ns, "/config/var.redefine", True)
    nsSet(ns, "/config/path", ["/home", "/bin", "/sbin"])
    return ns
