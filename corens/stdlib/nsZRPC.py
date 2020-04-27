from corens.console import nsconsole
from corens.ns import *


def nsZRpcInit(ns, *args, **kw):
    if len(nsGet(ns, "/etc/zrpc")) == 0:
        return
    nsconsole(ns, "ZRPC start")
    for r in nsGet(ns, "/etc/zrpc"):
        nsconsole(ns, "ZRPC(user) service {} on {}".format(r, nsGet(ns, "/etc/zrpc")[r]))
        if listenHost is None:
            nsconsole(ns, "Failed to parse {}".format(nsGet(ns, "/etc/zrpc")[r]))
            continue
        if nsRPCBringupServer(ns, "/usr/local/rpc/user/{}".format(r),
                nsGet(ns, "/etc/zrpc")[r],
                nsGet(ns, "/config/defaultZRPCMax")) is not True:
            nsError(ns, "Unable to bring up {}:{} ZRPC server".format(listenHost, listenPort))



def nsZRpcStop(ns, *args, **kw):
    if len(nsGet(ns, "/etc/rpc")) == 0:
        return
    nsconsole(ns, "ZRPC stop")


_init = [
    "z96_rpc"
]

_actions = {
    "z96_rpc": {
        "start" : nsZRpcInit,
        "stop" : nsZRpcStop
    }
}
