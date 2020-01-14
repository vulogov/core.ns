from corens.ns import *

def n(ns):
    return ns

_lib = {
    '/bin/mkdir': nsMkdir,
    '/bin/get': nsGet,
    '/bin/set': nsSet,
    '/bin/ls': nsLs,
    '/bin/ns': n
}
