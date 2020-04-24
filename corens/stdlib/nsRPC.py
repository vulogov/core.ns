import json
from corens.console import nsconsole
from corens.log import *
from corens.rpc import *
from corens.ns import *
from corens.sec import *


def nsRpcInit(ns, *args, **kw):
    nsconsole(ns, "RPC start")
    for r in nsGet(ns, "/etc/rpc"):
        nsconsole(ns, "RPC service {} on {}".format(r, nsGet(ns, "/etc/rpc")[r]))
        #if nsRPCBringupServer(ns, "/usr/local/rpc/user/{}".format(r)) is not True:
        #    nsError(ns, "Unable to bring up RPC {}".format(r))


def nsRpcStop(ns, *args, **kw):
    nsconsole(ns, "RPC stop")

def nsInternalServerStart(ns, *args, **kw):
    nsconsole(ns, "INTERNAL RPC start")
    if nsGet(ns, "/etc/flags/internalServer", False) is True:
        nsconsole(ns, "Internal RPC server enabled")
        if nsRPCBringupServer(ns, "/usr/local/rpc/internal",
                nsGet(ns, "/config/defaultInternalListen"),
                nsGet(ns, "/config/defaultInternalPort"),
                nsGet(ns, "/config/defaultInternalMax")) is not True:
            nsError(ns, "Unable to bring up internal RPC server")
    else:
        nsconsole(ns, "Internal RPC server disabled")

def nsInternalServerStop(ns, *args, **kw):
    nsconsole(ns, "INTERNAL RPC stop")

def nsInternalServerGet(ns, cookie, path):
    if nsCookie(ns, cookie) is False:
        return {'err': True, 'msg':'Authentication failed'}
    if path[-1] == '/':
        return nsDir(ns, path)
    res = nsGet(ns, path)
    if isinstance(res, dict) is True and '__dir__' in res and res['__dir__'] is True:
        return nsDir(ns, path)
    return res

_mkdir = [
    "/usr/local/rpc/internal",
    "/usr/local/rpc/internal/handlers",
    "/usr/local/rpc/user"
]

_init = [
    "rpc", "internal"
]

_actions = {
    "rpc": {
        "start" : nsRpcInit,
        "stop" : nsRpcStop
    },
    "internal": {
        "start": nsInternalServerStart,
        "stop": nsInternalServerStop
    }
}

_lib = {
    "/usr/local/rpc/internal/handlers/get" : nsInternalServerGet,
}
