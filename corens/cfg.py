from fs.opener import open_fs
from corens.ns import *
from corens.cfg_grammar import nsCfgGrammar

def nsDefaults(ns):
    nsSet(ns, "/config/var.redefine", True)
    nsSet(ns, "/config/path", ["/home", "/bin", "/sbin"])
    nsSet(ns, "/config/dev.path", "/dev")
    nsSet(ns, "/config/cfg.path", ['osfs://.','osfs://tests'])
    nsSet(ns, "/config/cfg.fs", [])
    nsSet(ns, "/config/cfg.files", [])
    nsSet(ns, "/config/library", ["corens.stdlib"])
    nsSet(ns, "/config/answer", 42)
    for c in nsGet(ns, "/config/cfg.path"):
        nsGet(ns, "/config/cfg.fs").append(open_fs(c))
    ns = nsCfgGrammar(ns)
    return ns
