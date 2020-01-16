from collections.abc import Callable
from toolz import partial
from corens.ns import *

def nsTemplate(ns, name, **kw):
    path = "/templates/{}".format(name)
    ctx = nsMkdir(ns, path)
    for k in kw:
        _path =  "{}/{}".format(path, k)
        nsSet(ns, _path, kw[k])
    return ns

def nsMk(ns, name):
    dev_path = nsGet(ns, "/config/dev/path", "/dev")
    _path = "{}/{}".format(dev_path, name)
    _t = nsGet(ns, "/templates/{}".format(name))
    ctx = nsMkdir(ns, _path)
    for i in _t:
        _i = "{}/{}".format(_path, i)
        if isinstance(_t[i], Callable) is True:
            nsSet(ns, _i, partial(_t[i], ns, ctx))
        else:
            nsSet(ns, _i, _t[i])
    _init = nsGet(ns, "{}/{}/init".format(dev_path, name), None)
    if _init is not None and isinstance(_init, Callable) is True:
        ns = _init()
    return ns
