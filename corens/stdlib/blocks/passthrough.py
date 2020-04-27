from uuid import uuid4
from toolz import partial
from gevent.queue import Queue
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon

def nsBlockPassInit(ns):
    nsSet(ns, "/blocks/pass/in", partial(nsGet(ns, "/usr/local/blocks/pass/in"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/inF", partial(nsGet(ns, "/usr/local/blocks/pass/inF"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/out", partial(nsGet(ns, "/usr/local/blocks/pass/out"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/outF", partial(nsGet(ns, "/usr/local/blocks/pass/outF"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/create", partial(nsGet(ns, "/usr/local/blocks/pass/task"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/server", partial(nsGet(ns, "/usr/local/blocks/pass/server"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/handler", partial(nsGet(ns, "/usr/local/blocks/pass/handler"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/call", partial(nsGet(ns, "/usr/local/blocks/pass/call"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/exists", partial(nsGet(ns, "/usr/local/blocks/pass/exists"), "/blocks/pass"))
    nsSet(ns, "/blocks/pass/configured", True)
    return True

def nsBlockPassTask(ns, block_path, name, _handler=None, **kw):
    task_path = "/tasks/pass/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/blocking".format(task_path), False)
    nsSet(ns, "{}/in_q".format(task_path), Queue())
    nsSet(ns, "{}/out_q".format(task_path), Queue())
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/pass/in"), task_path))
    nsSet(ns, "{}/inF".format(task_path), partial(nsGet(ns, "/blocks/pass/inF"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/pass/out"), task_path))
    nsSet(ns, "{}/outF".format(task_path), partial(nsGet(ns, "/blocks/pass/outF"), task_path))


    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/pass/server"), task_path))
    if _handler is None:
        nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/pass/handler"), task_path))
    else:
        nsSet(ns, "{}/handler".format(task_path), partial(_handler, block_path, task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/pass/call"), task_path))
    for k in kw:
        nsSet(ns, "{}/{}".format(task_path, k), kw[k])
    nsDaemon(ns, "TASK:pass:{}".format(name), nsGet(ns, "{}/server".format(task_path)), _raw=True)
    return True

def nsBlockPassIn(ns, block_path, task_path, data):
    nsGet(ns, "{}/in_q".format(task_path)).put_nowait(data)
    return data
def nsBlockPassInGet(ns, block_path, task_path):
    q = nsGet(ns, "{}/in_q".format(task_path))
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is True:
        return q.get()
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is False:
        return None
    return q.get_nowait()

def nsBlockPassOut(ns, block_path, task_path, data):
    nsGet(ns, "{}/out_q".format(task_path)).put_nowait(data)
    return data
def nsBlockPassOutGet(ns, block_path, task_path):
    q = nsGet(ns, "{}/out_q".format(task_path))
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is True:
        return q.get()
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is False:
        return None
    return q.get_nowait()

def nsBlockPassServer(ns, block_path, task_path):
    return

def nsBlockPassExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/pass")


_mkdir = [
    "/usr/local/blocks/pass",
    "/blocks/pass",
    "/tasks/pass",
]

_lib = {
    "/usr/local/blocks/pass/init" : nsBlockPassInit,
    "/usr/local/blocks/pass/task": nsBlockPassTask,
    "/usr/local/blocks/pass/in": nsBlockPassIn,
    "/usr/local/blocks/pass/inF": nsBlockPassInGet,
    "/usr/local/blocks/pass/outF": nsBlockPassOut,
    "/usr/local/blocks/pass/out": nsBlockPassOutGet,
    "/usr/local/blocks/pass/server": nsBlockLoopSimple,
    "/usr/local/blocks/pass/handler": nsBlockNullHandler,
    "/usr/local/blocks/pass/call": nsBlockNullCall,
    "/usr/local/blocks/pass/exists": nsBlockPassExists,
    "/usr/local/blocks/pass/running": nsBlockPassExists,
}
