from uuid import uuid4
from toolz import partial
from gevent.queue import Queue
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon
from corens.stdlib.blocks.passthrough import nsBlockPassOutEmpty, nsBlockPassIn, nsBlockPassOut, nsBlockPassInGet, nsBlockPassOutGet

def nsBlockFilterInit(ns):
    nsSet(ns, "/blocks/filter/in", partial(nsGet(ns, "/usr/local/blocks/filter/in"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/inF", partial(nsGet(ns, "/usr/local/blocks/filter/inF"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/out", partial(nsGet(ns, "/usr/local/blocks/filter/out"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/outF", partial(nsGet(ns, "/usr/local/blocks/filter/outF"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/create", partial(nsGet(ns, "/usr/local/blocks/filter/task"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/server", partial(nsGet(ns, "/usr/local/blocks/filter/server"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/handler", partial(nsGet(ns, "/usr/local/blocks/filter/handler"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/reject", partial(nsGet(ns, "/usr/local/blocks/filter/reject"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/call", partial(nsGet(ns, "/usr/local/blocks/filter/call"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/empty", partial(nsGet(ns, "/usr/local/blocks/filter/empty"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/exists", partial(nsGet(ns, "/usr/local/blocks/filter/exists"), "/blocks/filter"))
    nsSet(ns, "/blocks/filter/configured", True)
    return True

def nsBlockFilterTask(ns, block_path, name, _handler=None, _reject=None, **kw):
    task_path = "/tasks/filter/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/blocking".format(task_path), False)
    nsSet(ns, "{}/in_q".format(task_path), Queue())
    nsSet(ns, "{}/out_q".format(task_path), Queue())
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/filter/in"), task_path))
    nsSet(ns, "{}/inF".format(task_path), partial(nsGet(ns, "/blocks/filter/inF"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/filter/out"), task_path))
    nsSet(ns, "{}/outF".format(task_path), partial(nsGet(ns, "/blocks/filter/outF"), task_path))
    nsSet(ns, "{}/empty".format(task_path), partial(nsGet(ns, "/blocks/filter/empty"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/filter/server"), task_path))
    if _handler is None:
        nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/filter/handler"), task_path))
    else:
        nsSet(ns, "{}/handler".format(task_path), partial(_handler, block_path, task_path))
    if _reject is None:
        nsSet(ns, "{}/reject".format(task_path), partial(nsGet(ns, "/blocks/filter/reject"), task_path))
    else:
        nsSet(ns, "{}/reject".format(task_path), partial(_reject, block_path, task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/filter/call"), task_path))
    for k in kw:
        nsSet(ns, "{}/{}".format(task_path, k), kw[k])
    nsDaemon(ns, "TASK:filter:{}".format(name), nsGet(ns, "{}/server".format(task_path)), _raw=True)
    return True


def nsBlockFilterExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/filter")

def nsBlockFilterRunning(ns, block_path, name):
    return "TASK:filter:{}".format(name) in nsDir(ns, "/proc")


_mkdir = [
    "/usr/local/blocks/filter",
    "/blocks/filter",
    "/tasks/filter",
]

_lib = {
    "/usr/local/blocks/filter/init" : nsBlockFilterInit,
    "/usr/local/blocks/filter/task": nsBlockFilterTask,
    "/usr/local/blocks/filter/in": nsBlockPassIn,
    "/usr/local/blocks/filter/inF": nsBlockPassInGet,
    "/usr/local/blocks/filter/outF": nsBlockPassOut,
    "/usr/local/blocks/filter/out": nsBlockPassOutGet,
    "/usr/local/blocks/filter/server": nsBlockLoopFilter,
    "/usr/local/blocks/filter/handler": nsBlockNullTrue,
    "/usr/local/blocks/filter/reject": nsBlockNullHandler,
    "/usr/local/blocks/filter/call": nsBlockNullCall,
    "/usr/local/blocks/filter/empty": nsBlockPassOutEmpty,
    "/usr/local/blocks/filter/exists": nsBlockFilterExists,
    "/usr/local/blocks/filter/running": nsBlockFilterRunning,
}
