from uuid import uuid4
from toolz import partial
from gevent.queue import Queue
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon

from corens.stdlib.blocks.passthrough import nsBlockPassOut, nsBlockPassOutGet, nsBlockPassOutEmpty
from corens.stdlib.blocks.null import nsBlockNullIn, nsBlockNullOut

def nsBlockEmitInit(ns):
    nsSet(ns, "/blocks/emit/in", partial(nsGet(ns, "/usr/local/blocks/emit/in"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/inF", partial(nsGet(ns, "/usr/local/blocks/emit/inF"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/out", partial(nsGet(ns, "/usr/local/blocks/emit/out"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/outF", partial(nsGet(ns, "/usr/local/blocks/emit/outF"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/create", partial(nsGet(ns, "/usr/local/blocks/emit/task"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/server", partial(nsGet(ns, "/usr/local/blocks/emit/server"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/handler", partial(nsGet(ns, "/usr/local/blocks/emit/handler"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/call", partial(nsGet(ns, "/usr/local/blocks/emit/call"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/empty", partial(nsGet(ns, "/usr/local/blocks/emit/empty"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/exists", partial(nsGet(ns, "/usr/local/blocks/emit/exists"), "/blocks/emit"))
    nsSet(ns, "/blocks/emit/configured", True)
    return True

def nsBlockEmitTask(ns, block_path, name, _handler=None, **kw):
    task_path = "/tasks/emit/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/blocking".format(task_path), False)
    nsSet(ns, "{}/out_q".format(task_path), Queue())
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/emit/in"), task_path))
    nsSet(ns, "{}/inF".format(task_path), partial(nsGet(ns, "/blocks/emit/inF"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/emit/out"), task_path))
    nsSet(ns, "{}/outF".format(task_path), partial(nsGet(ns, "/blocks/emit/outF"), task_path))
    nsSet(ns, "{}/empty".format(task_path), partial(nsGet(ns, "/blocks/emit/empty"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/emit/server"), task_path))
    if _handler is None:
        nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/emit/handler"), task_path))
    else:
        nsSet(ns, "{}/handler".format(task_path), partial(_handler, block_path, task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/emit/call"), task_path))
    for k in kw:
        nsSet(ns, "{}/{}".format(task_path, k), kw[k])
    nsDaemon(ns, "TASK:emit:{}".format(name), nsGet(ns, "{}/server".format(task_path)), _raw=True)
    return True



def nsBlockEmitOut(ns, block_path, task_path, data):
    nsGet(ns, "{}/out_q".format(task_path)).put_nowait(data)
    return data
def nsBlockEmitOutGet(ns, block_path, task_path):
    q = nsGet(ns, "{}/out_q".format(task_path))
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is True:
        return q.get()
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is False:
        return None
    return q.get_nowait()


def nsBlockEmitExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/emit")

def nsBlockEmitRunning(ns, block_path, name):
    return "TASK:emit:{}".format(name) in nsDir(ns, "/proc")

_mkdir = [
    "/usr/local/blocks/emit",
    "/blocks/emit",
    "/tasks/emit",
]

_lib = {
    "/usr/local/blocks/emit/init" : nsBlockEmitInit,
    "/usr/local/blocks/emit/task": nsBlockEmitTask,
    "/usr/local/blocks/emit/in": nsBlockNullIn,
    "/usr/local/blocks/emit/inF": nsBlockNullOut,
    "/usr/local/blocks/emit/outF": nsBlockPassOut,
    "/usr/local/blocks/emit/out": nsBlockPassOutGet,
    "/usr/local/blocks/emit/server": nsBlockLoopEmit,
    "/usr/local/blocks/emit/handler": nsBlockNullHandler,
    "/usr/local/blocks/emit/call": nsBlockNullCall,
    "/usr/local/blocks/emit/empty": nsBlockPassOutEmpty,
    "/usr/local/blocks/emit/exists": nsBlockEmitExists,
    "/usr/local/blocks/emit/running": nsBlockEmitRunning,
}
