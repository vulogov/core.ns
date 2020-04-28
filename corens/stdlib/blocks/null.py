from uuid import uuid4
from toolz import partial
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon

def nsBlockNullInit(ns):
    nsSet(ns, "/blocks/null/in", partial(nsGet(ns, "/usr/local/blocks/null/in"), "/blocks/null"))
    nsSet(ns, "/blocks/null/out", partial(nsGet(ns, "/usr/local/blocks/null/out"), "/blocks/null"))
    nsSet(ns, "/blocks/null/create", partial(nsGet(ns, "/usr/local/blocks/null/task"), "/blocks/null"))
    nsSet(ns, "/blocks/null/server", partial(nsGet(ns, "/usr/local/blocks/null/server"), "/blocks/null"))
    nsSet(ns, "/blocks/null/handler", partial(nsGet(ns, "/usr/local/blocks/null/handler"), "/blocks/null"))
    nsSet(ns, "/blocks/null/call", partial(nsGet(ns, "/usr/local/blocks/null/call"), "/blocks/null"))
    nsSet(ns, "/blocks/null/exists", partial(nsGet(ns, "/usr/local/blocks/null/exists"), "/blocks/null"))
    nsSet(ns, "/blocks/null/configured", True)
    return True

def nsBlockNullTask(ns, block_path, name):
    task_path = "/tasks/null/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/null/in"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/null/out"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/null/server"), task_path))
    nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/null/handler"), task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/null/call"), task_path))
    nsDaemon(ns, "TASK:null:{}".format(name), nsGet(ns, "{}/server".format(task_path)))
    return True

def nsBlockNullIn(ns, block_path, task_path, data):
    return data

def nsBlockNullOut(ns, block_path, task_path):
    return None

def nsBlockNullExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/null")


_mkdir = [
    "/usr/local/blocks/null",
    "/blocks/null",
    "/tasks/null",
]

_lib = {
    "/usr/local/blocks/null/init" : nsBlockNullInit,
    "/usr/local/blocks/null/task": nsBlockNullTask,
    "/usr/local/blocks/null/in": nsBlockNullIn,
    "/usr/local/blocks/null/out": nsBlockNullOut,
    "/usr/local/blocks/null/server": nsBlockNullServer,
    "/usr/local/blocks/null/handler": nsBlockNullHandler,
    "/usr/local/blocks/null/call": nsBlockNullCall,
    "/usr/local/blocks/null/exists": nsBlockNullExists,
    "/usr/local/blocks/null/running": nsBlockNullExists,
}
