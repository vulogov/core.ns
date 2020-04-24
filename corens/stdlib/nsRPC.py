import json
import time
from corens.console import nsconsole
from corens.log import *
from corens.rpc import *
from corens.ns import *
from corens.sec import *
from corens.hylang import nsHyEvalRestrict, nsHyPipelineRestrict
from corens.gevt import nsSchedulerPS, nsSchedulerIntervalJob, nsKillAll

def nsRPCExec(ns, dev_path, cookie, name, *args, **kw):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    if name in nsLs(ns, "{}/root".format(dev_path)):
        return nsGet(ns, "{}/root/{}".format(dev_path, name))(*args, **kw)
    return {'err': True, 'msg':'Command {} not found'.format(name)}

def nsRPCHy(ns, dev_path, cookie, expr):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    if "root" in nsLs(ns, dev_path):
        dev_path = "{}/root".format(dev_path)
    return nsHyEvalRestrict(ns, expr, dev_path)

def nsRPCHyPipe(ns, dev_path, cookie, expr):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    if "root" in nsLs(ns, dev_path):
        dev_path = "{}/root".format(dev_path)
    return nsHyPipelineRestrict(ns, expr, dev_path)

def nsRpcInit(ns, *args, **kw):
    nsconsole(ns, "RPC start")
    for r in nsGet(ns, "/etc/rpc"):
        nsconsole(ns, "RPC service {} on {}".format(r, nsGet(ns, "/etc/rpc")[r]))
        #if nsRPCBringupServer(ns, "/usr/local/rpc/user/{}".format(r)) is not True:
        #    nsError(ns, "Unable to bring up RPC {}".format(r))


def nsRpcStop(ns, *args, **kw):
    nsconsole(ns, "RPC stop")

def nsInternalServerShutdownWatcher(ns):
    if nsGet(ns, "/etc/shutdownRequested") is True:
        nsconsole(ns, "Shutdown is executing")
        nsKillAll(ns)

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
    nsSchedulerIntervalJob(ns, 15, "ShutdownWatcher", nsInternalServerShutdownWatcher)

def nsInternalServerStop(ns, *args, **kw):
    nsconsole(ns, "INTERNAL RPC stop")

def nsInternalServerGet(ns, dev_path, cookie, path):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    if path[-1] == '/':
        return nsDir(ns, path)
    res = nsGet(ns, path)
    if isinstance(res, dict) is True and '__dir__' in res and res['__dir__'] is True:
        return nsDir(ns, path)
    return res

def nsInternalServerPS(ns, dev_path, cookie):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    out = {}
    for p in nsLs(ns, "/proc"):
        out[p] = nsGet(ns, "/proc/{}/stamp".format(p))
    return out

def nsInternalServerScheduler(ns, dev_path, cookie):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    out = {}
    for i in nsSchedulerPS(ns):
        out[i.name] =  str(i.next_run_time)
    return out

def nsInternalServerTick(ns, dev_path, cookie):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    return nsGet(ns, "/dev/time")

def nsInternalServerShutdown(ns, dev_path, cookie):
    #if nsCookie(ns, cookie) is False:
    #    return {'err': True, 'msg':'Authentication failed'}
    nsInfo(ns, "Shutdown has been requested from internal server")
    nsSet(ns, "/etc/shutdownRequested", True)
    return nsGet(ns, "/etc/shutdownRequested")

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

_ln = {
    '/bin/rpcexecutor' : "/usr/local/rpc/internal/handlers/exec",
    '/bin/rpchy' : "/usr/local/rpc/internal/handlers/hy",
    '/bin/rpchy|' : "/usr/local/rpc/internal/handlers/hy|",
}
_lib = {
    "/bin/rpcexecutor": nsRPCExec,
    "/bin/rpchy": nsRPCHy,
    "/bin/rpchy|": nsRPCHyPipe,
    "/usr/local/rpc/internal/jail" : ["/bin/id", "/bin/stamp"],
    "/usr/local/rpc/internal/handlers/get" : nsInternalServerGet,
    "/usr/local/rpc/internal/handlers/ps" : nsInternalServerPS,
    "/usr/local/rpc/internal/handlers/scheduler" : nsInternalServerScheduler,
    "/usr/local/rpc/internal/handlers/tick" : nsInternalServerTick,
    "/usr/local/rpc/internal/handlers/shutdown" : nsInternalServerShutdown,
}
