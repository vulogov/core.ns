import os.path
import gevent
import json
import re
import gevent.pywsgi
import gevent.queue
import gevent.pool

from toolz import partial
from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

from corens.ns import *
from corens.log import *
from corens.console import nsConsole, nsConsolePush
from corens.gevt import nsDaemon

def nsParseListen(ns, s):
    if s[0] == ":":
        if re.match(r"(\s*)(\d+)(\s*)", s[1:]) is not None:
            _p = int(s[1:])
        else:
            return (None,None)
        return (nsGet(ns, "/etc/defaultRPCListen", "127.0.0.1"), _p)
    else:
        if re.match(r"^(\s*)(.*)(\s*)\:(\s*)(\d+)(\s*)", s) is not None:
            p = re.split(r"^(\s*)(.*)(\s*)\:(\s*)(\d+)(\s*)", s)
            return (p[2], int(p[5]))
    return (None,None)

def nsRPCisServer(ns, path):
    _ls = nsLs(ns, path)
    if "handlers" not in _ls:
        return False
    return True

def nsRPCCatcher(ns, dev_path, _queue, *args):
    _d = json.loads(args[2])
    _d["dir"] = args[0]
    _d["path"] = dev_path
    _queue.put(_d)
    if nsGet(ns, "/etc/flags/rpctraceconsole", False) is True:
        nsConsolePush(ns, _d)

def nsRPCBringupServer(ns, path, host, port, maxconn):
    name = os.path.basename(path)
    dev_path = '/dev/rpc/{}'.format(name)
    if nsRPCisServer(ns, path) is not True:
        nsError(ns, "RPC service {} misconfigured".format(name))
        return False
    nsInfo(ns, "Configuring RPC server from {}".format(path))
    nsMkdir(ns, dev_path)
    nsMkdir(ns, "{}/root".format(dev_path))
    _to_root = nsGet(ns, "{}/jail".format(path), [])
    for j in _to_root:
        _n = os.path.basename(j)
        _dst = "{}/root/{}".format(dev_path, _n)
        nsInfo(ns, "RPC.JAIL({}): {}".format(name, j))
        nsLn(ns, j, _dst)
    dispatcher = RPCDispatcher()
    nsSet(ns, "{}/dispatcher".format(dev_path), dispatcher)
    for h in nsLs(ns, "{}/handlers".format(path)):
        nsInfo(ns, "Registering {}->{} ".format(name, h))
        _fun = nsGet(ns, "{}/handlers/{}".format(path, h))
        dispatcher.add_method(partial(_fun, dev_path), h)
    transport = WsgiServerTransport(queue_class=gevent.queue.Queue)
    nsSet(ns, "{}/transport".format(dev_path), transport)
    nsSet(ns, "{}/listen".format(dev_path), host)
    nsSet(ns, "{}/port".format(dev_path), host)
    nsConsole(ns, "RPC server {} will be listening on tcp://{}:{}".format(name, host, port))
    pool = gevent.pool.Pool(maxconn)
    nsSet(ns, "{}/pool".format(dev_path), pool)
    wsgi_server = gevent.pywsgi.WSGIServer((host, port), transport.handle, spawn=pool, log=None)
    nsSet(ns, "{}/wsgi".format(dev_path), wsgi_server)
    nsDaemon(ns, "{}:WSGI".format(name), wsgi_server.serve_forever, _raw=True)
    rpc_server = RPCServerGreenlets(
        transport,
        JSONRPCProtocol(),
        dispatcher
    )
    if nsGet(ns, "/config/RPCCatchCalls") is True or nsGet(ns, "/etc/flags/rpctrace", False) is True:
        _q = gevent.queue.Queue()
        nsSet(ns, "{}/trace".format(dev_path), _q)
        rpc_server.trace = partial(nsRPCCatcher, ns, dev_path, _q)
    nsSet(ns, "{}/rpc", rpc_server)
    nsDaemon(ns, "{}:RPC".format(name), rpc_server.serve_forever, _raw=True)
    nsInfo(ns, "RPC server {} is up".format(name))
    return True
