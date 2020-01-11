from toolz import partial
from corens.ns import NS as _NS
from corens.mod import F as _F

def NS():
    from corens.mod import nsImport
    ns = _NS()
    ns = nsImport(ns, 'corens.stdlib')
    return (ns, partial(_F, ns))
