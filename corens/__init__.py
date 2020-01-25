from gevent import monkey
if monkey.patch_all() is not True:
    print("Gevent monkey patching was not succesful")
import sys
from toolz import partial
from corens.ns import NS as _NS
from corens.ns import nsGet
from corens.mod import F as _F
from corens.mod import f as _f

from corens.cfg import nsDefaults

def NS(*args, **kw):
    from corens.mod import nsImport
    ns = _NS()
    ns = nsDefaults(ns)
    ns = nsImport(ns, nsGet(ns, "/config/library"))
    for c in nsGet(ns, "/config/cfg.files"):
        _f(ns, "/bin/Cfg")(c)
    ns = nsImport(ns, nsGet(ns, "/config/user.library"))
    cargs = kw.get('args', None)
    if cargs is None:
        cargs = sys.argv[1:]
    _f(ns, "/bin/args")(cargs)
    _f(ns, "/bin/gevent")()
    _f(ns, "/sbin/vnsinit")()
    _f(ns, "/bin/cmd")
    return (ns, partial(_f, ns), partial(_F, ns))
