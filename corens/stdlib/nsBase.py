from corens.ns import *
from corens.mod import I, nsImport
from corens.tpl import nsTemplate, nsMk

def n(ns):
    return ns

_lib = {
    '/bin/mkdir': nsMkdir,
    '/bin/get': nsGet,
    '/bin/set': nsSet,
    '/bin/ls': nsLs,
    '/bin/ns': n,
    '/bin/V': V,
    '/bin/I': I,
    '/bin/import': nsImport,
    '/bin/T': nsTemplate,
    '/bin/Mk': nsMk
}
