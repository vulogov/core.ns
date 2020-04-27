import zmq.green as zmq

from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from corens.rpm import nsRPCisServer

def nsZRPCBringupServer(ns, path, conn, maxconn):
    name = os.path.basename(path)
    dev_path = '/dev/zrpc/{}'.format(name)
    if nsRPCisServer(ns, path) is not True:
        nsError(ns, "ZRPC service {} misconfigured".format(name))
        return False
    nsInfo(ns, "Configuring ZRPC server from {}".format(path))
    nsMkdir(ns, dev_path)
    nsMkdir(ns, "{}/root".format(dev_path))
    _to_root = nsGet(ns, "{}/jail".format(path), [])
    for j in _to_root:
        _n = os.path.basename(j)
        _dst = "{}/root/{}".format(dev_path, _n)
        nsInfo(ns, "ZRPC.JAIL({}): {}".format(name, j))
        nsLn(ns, j, _dst)

    dispatcher = RPCDispatcher()
    nsSet(ns, "{}/dispatcher".format(dev_path), dispatcher)
    for h in nsLs(ns, "{}/handlers".format(path)):
        nsInfo(ns, "Registering {}->{} ".format(name, h))
        _fun = nsGet(ns, "{}/handlers/{}".format(path, h))
        dispatcher.add_method(partial(_fun, dev_path), h)

    transport = ZmqServerTransport.create(ctx, conn)
    nsSet(ns, "{}/transport".format(dev_path), transport)
    nsSet(ns, "{}/conn".format(dev_path), conn)
    rpc_server = RPCServerGreenlets(
        transport,
        JSONRPCProtocol(),
        dispatcher
    )
    nsSet(ns, "{}/rpc", rpc_server)
    nsDaemon(ns, "{}:ZRPC".format(name), rpc_server.serve_forever, _raw=True)
    nsInfo(ns, "ZRPC server {} is up".format(name))
    return True
