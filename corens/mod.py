import builtins
import os.path
import pkgutil
import importlib
from toolz import partial
from corens.ns import *
from corens.log import *

def nsImport(ns, module):
    for loader, module_name, is_pkg in pkgutil.walk_packages(importlib.import_module(module).__path__):
        _module = loader.find_module(module_name).load_module(module_name)
        try:
            _lib = getattr(_module, '_lib')
        except AttributeError:
            nsError(ns, "Module %(module)s is missing description", module=module_name)
            continue
        for k in _lib:
            nsSet(ns, k, partial(_lib[k], ns))
    return ns

def f(ns, name):
    if name[0] == "/":
        fun = nsGet(ns, name, None)
        if fun is None:
            nsError(ns, "Call for unknown full-path function %(fun)s", fun=name)
            return None
        return fun
    for p in ["/home", "/bin", "/sbin"]:
        fun = nsGet(ns, "{}/{}".format(p, name), None)
        if fun is None:
            continue
        return fun
    nsError(ns, "Call for unknown function %(fun)s", fun=name)
    return None

def F(ns, *funcs):
    for _f in funcs:
        _nf = f(ns, _f)
        if _nf is None:
            continue
        setattr(builtins, os.path.basename(_f), _nf)
    return ns
