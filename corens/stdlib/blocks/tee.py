from uuid import uuid4
from toolz import partial
from gevent.queue import Queue
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon
from corens.stdlib.blocks.passthrough import nsBlockPassOutEmpty, nsBlockPassIn, nsBlockPassOut, nsBlockPassInGet, nsBlockPassOutGet


def nsBlockTeeInit(ns):
    nsSet(ns, "/blocks/tee/in", partial(nsGet(ns, "/usr/local/blocks/tee/in"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/inF", partial(nsGet(ns, "/usr/local/blocks/tee/inF"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/out", partial(nsGet(ns, "/usr/local/blocks/tee/out"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/outF", partial(nsGet(ns, "/usr/local/blocks/tee/outF"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/create", partial(nsGet(ns, "/usr/local/blocks/tee/task"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/server", partial(nsGet(ns, "/usr/local/blocks/tee/server"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/handler", partial(nsGet(ns, "/usr/local/blocks/tee/handler"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/call", partial(nsGet(ns, "/usr/local/blocks/tee/call"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/empty", partial(nsGet(ns, "/usr/local/blocks/tee/empty"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/monitor", partial(nsGet(ns, "/usr/local/blocks/tee/monitor"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/exists", partial(nsGet(ns, "/usr/local/blocks/tee/exists"), "/blocks/tee"))
    nsSet(ns, "/blocks/tee/configured", True)
    return True

def nsBlockTeeTask(ns, block_path, name, _handler=None, **kw):
    task_path = "/tasks/tee/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/blocking".format(task_path), False)
    nsSet(ns, "{}/in_q".format(task_path), Queue())
    nsSet(ns, "{}/out_q".format(task_path), Queue())
    nsSet(ns, "{}/_monitor".format(task_path), Queue())
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/tee/in"), task_path))
    nsSet(ns, "{}/inF".format(task_path), partial(nsGet(ns, "/blocks/tee/inF"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/tee/out"), task_path))
    nsSet(ns, "{}/outF".format(task_path), partial(nsGet(ns, "/blocks/tee/outF"), task_path))
    nsSet(ns, "{}/empty".format(task_path), partial(nsGet(ns, "/blocks/tee/empty"), task_path))
    nsSet(ns, "{}/monitor".format(task_path), partial(nsGet(ns, "/blocks/tee/monitor"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/tee/server"), task_path))
    if _handler is None:
        nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/tee/handler"), task_path))
    else:
        nsSet(ns, "{}/handler".format(task_path), partial(_handler, block_path, task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/tee/call"), task_path))
    for k in kw:
        nsSet(ns, "{}/{}".format(task_path, k), kw[k])
    nsDaemon(ns, "TASK:tee:{}".format(name), nsGet(ns, "{}/server".format(task_path)), _raw=True)
    return True

def nsBlockTeeHandler(ns, block_path, task_path,  data,  *args, **kw):
    nsGet(ns, "{}/_monitor".format(task_path)).put_nowait(data)
    return data

def nsBlockTeeMonitor(ns, block_path, task_path):
    return nsBlockQueueGet(ns, block_path, task_path, "{}/_monitor".format(task_path))

def nsBlockTeeExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/tee")

def nsBlockTeeRunning(ns, block_path, name):
    return "TASK:tee:{}".format(name) in nsDir(ns, "/proc")

_mkdir = [
    "/usr/local/blocks/tee",
    "/blocks/tee",
    "/tasks/tee",
]

_lib = {
    "/usr/local/blocks/tee/init" : nsBlockTeeInit,
    "/usr/local/blocks/tee/task": nsBlockTeeTask,
    "/usr/local/blocks/tee/in": nsBlockPassIn,
    "/usr/local/blocks/tee/inF": nsBlockPassInGet,
    "/usr/local/blocks/tee/outF": nsBlockPassOut,
    "/usr/local/blocks/tee/out": nsBlockPassOutGet,
    "/usr/local/blocks/tee/server": nsBlockLoopSimple,
    "/usr/local/blocks/tee/handler": nsBlockTeeHandler,
    "/usr/local/blocks/tee/call": nsBlockNullCall,
    "/usr/local/blocks/tee/empty": nsBlockPassOutEmpty,
    "/usr/local/blocks/tee/monitor": nsBlockTeeMonitor,
    "/usr/local/blocks/tee/exists": nsBlockTeeExists,
    "/usr/local/blocks/tee/running": nsBlockTeeRunning,
}
