from corens.ns import *

def nsDefaults(ns):
    nsSet(ns, "/config/var.redefine", True)
    nsSet(ns, "/config/path", ["/home", "/bin", "/sbin"])
    nsSet(ns, "/config/dev.path", "/dev")
    nsSet(ns, "/config/library", ["corens.stdlib"])
    nsSet(ns, "/config/answer", 42)
    return ns
