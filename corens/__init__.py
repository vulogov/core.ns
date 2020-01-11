from toolz import partial
from corens.ns import NS as _NS
from corens.mod import F as _F
from corens.mod import f as _f


def NS():
    from corens.mod import nsImport
    ns = _NS()
    ns = nsImport(ns, 'corens.stdlib')
    return (ns, partial(_f, ns), partial(_F, ns))
