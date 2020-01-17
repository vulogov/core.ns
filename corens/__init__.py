from gevent import monkey
monkey.patch_all() 
from toolz import partial
from corens.ns import NS as _NS
from corens.ns import nsGet
from corens.mod import F as _F
from corens.mod import f as _f

from corens.cfg import nsDefaults

def NS():
    from corens.mod import nsImport
    ns = _NS()
    ns = nsDefaults(ns)
    ns = nsImport(ns, nsGet(ns, "/config/library"))
    return (ns, partial(_f, ns), partial(_F, ns))
