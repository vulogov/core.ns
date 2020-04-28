from corens.console import nsconsole
from corens.log import *
from corens.ns import *
from textx import metamodel_from_str
import textx.exceptions

def nsMetaInit(ns, *args, **kw):
    if len(nsDir(ns, "/etc/meta")) == 0:
        return
    nsconsole(ns, "Metaprogramming start")
    for m in nsDir(ns, "/etc/meta"):
        nsInfo(ns, "Bringing metamodel {}".format(m))
        try:
            mm = metamodel_from_str(nsGet(ns, "/etc/meta/{}".format(m)), memoization=True)
        except (IndexError, textx.exceptions.TextXSyntaxError):
            nsError(ns, "Metamodel {} failed".format(m))
            continue
        nsSet(ns, "/meta/{}".format(m), mm)

def nsMetaStop(ns, *args, **kw):
    if len(nsDir(ns, "/etc/meta")) == 0:
        return
    nsconsole(ns, "Metaprogrammming stop")

_init = [
    "z80_metaprogramming"
]

_actions = {
    "z80_metaprogramming": {
        "start" : nsMetaInit,
        "stop" : nsMetaStop
    }
}
