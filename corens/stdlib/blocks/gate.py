from uuid import uuid4
from toolz import partial
from gevent.queue import Queue
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon
from corens.stdlib.blocks.passthrough import nsBlockPassOutEmpty, nsBlockPassIn, nsBlockPassOut, nsBlockPassInGet, nsBlockPassOutGet

def nsBlockGateInit(ns):
    nsSet(ns, "/blocks/gate/in", partial(nsGet(ns, "/usr/local/blocks/gate/in"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/inF", partial(nsGet(ns, "/usr/local/blocks/gate/inF"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/out", partial(nsGet(ns, "/usr/local/blocks/gate/out"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/outF", partial(nsGet(ns, "/usr/local/blocks/gate/outF"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/create", partial(nsGet(ns, "/usr/local/blocks/gate/task"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/server", partial(nsGet(ns, "/usr/local/blocks/gate/server"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/empty", partial(nsGet(ns, "/usr/local/blocks/gate/empty"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/call", partial(nsGet(ns, "/usr/local/blocks/gate/call"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/trigger", partial(nsGet(ns, "/usr/local/blocks/gate/trigger"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/exists", partial(nsGet(ns, "/usr/local/blocks/gate/exists"), "/blocks/gate"))
    nsSet(ns, "/blocks/gate/configured", True)
    return True

def nsBlockGateTask(ns, block_path, name, **kw):
    task_path = "/tasks/gate/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/blocking".format(task_path), False)
    nsSet(ns, "{}/gate".format(task_path), True)
    nsSet(ns, "{}/in_q".format(task_path), Queue())
    nsSet(ns, "{}/out_q".format(task_path), Queue())
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/gate/in"), task_path))
    nsSet(ns, "{}/inF".format(task_path), partial(nsGet(ns, "/blocks/gate/inF"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/gate/out"), task_path))
    nsSet(ns, "{}/outF".format(task_path), partial(nsGet(ns, "/blocks/gate/outF"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/gate/server"), task_path))
    nsSet(ns, "{}/trigger".format(task_path), partial(nsGet(ns, "/blocks/gate/trigger"), task_path))
    nsSet(ns, "{}/empty".format(task_path), partial(nsGet(ns, "/blocks/gate/empty"), task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/gate/call"), task_path))
    for k in kw:
        nsSet(ns, "{}/{}".format(task_path, k), kw[k])
    nsDaemon(ns, "TASK:gate:{}".format(name), nsGet(ns, "{}/server".format(task_path)), _raw=True)
    return True


def nsBlockGateExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/gate")

def nsBlockGateRunning(ns, block_path, name):
    return "TASK:gate:{}".format(name) in nsDir(ns, "/proc")

def nsBlockGateTrigger(ns, block_path, task_path):
    v = nsGet(ns, "{}/gate".format(task_path))
    nsSet(ns, "{}/gate".format(task_path), not v)
    return v


_mkdir = [
    "/usr/local/blocks/gate",
    "/blocks/gate",
    "/tasks/gate",
]

_lib = {
    "/usr/local/blocks/gate/init" : nsBlockGateInit,
    "/usr/local/blocks/gate/task": nsBlockGateTask,
    "/usr/local/blocks/gate/in": nsBlockPassIn,
    "/usr/local/blocks/gate/inF": nsBlockPassInGet,
    "/usr/local/blocks/gate/outF": nsBlockPassOut,
    "/usr/local/blocks/gate/out": nsBlockPassOutGet,
    "/usr/local/blocks/gate/server": nsBlockLoopGate,
    "/usr/local/blocks/gate/call": nsBlockNullCall,
    "/usr/local/blocks/gate/empty": nsBlockPassOutEmpty,
    "/usr/local/blocks/gate/trigger": nsBlockGateTrigger,
    "/usr/local/blocks/gate/exists": nsBlockGateExists,
    "/usr/local/blocks/gate/running": nsBlockGateRunning,
}
