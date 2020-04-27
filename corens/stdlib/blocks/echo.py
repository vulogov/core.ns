from uuid import uuid4
from toolz import partial
from corens.ns import *
from corens.block import *
from corens.gevt import nsDaemon

def nsBlockEchoInit(ns):
    nsSet(ns, "/blocks/echo/in", partial(nsGet(ns, "/usr/local/blocks/echo/in"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/out", partial(nsGet(ns, "/usr/local/blocks/echo/out"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/create", partial(nsGet(ns, "/usr/local/blocks/echo/task"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/server", partial(nsGet(ns, "/usr/local/blocks/echo/server"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/handler", partial(nsGet(ns, "/usr/local/blocks/echo/handler"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/call", partial(nsGet(ns, "/usr/local/blocks/echo/call"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/exists", partial(nsGet(ns, "/usr/local/blocks/echo/exists"), "/blocks/echo"))
    nsSet(ns, "/blocks/echo/configured", True)
    return True

def nsBlockEchoTask(ns, block_path, name):
    task_path = "/tasks/echo/{}".format(name)
    if name in nsDir(ns, task_path):
        return True
    nsMkdir(ns, task_path)
    nsSet(ns, "{}/id".format(task_path), str(uuid.uuid4()))
    nsSet(ns, "{}/args".format(task_path), ())
    nsSet(ns, "{}/kw".format(task_path), {})
    nsSet(ns, "{}/data".format(task_path), None)
    nsSet(ns, "{}/in".format(task_path), partial(nsGet(ns, "/blocks/echo/in"), task_path))
    nsSet(ns, "{}/out".format(task_path), partial(nsGet(ns, "/blocks/echo/out"), task_path))
    nsSet(ns, "{}/server".format(task_path), partial(nsGet(ns, "/blocks/echo/server"), task_path))
    nsSet(ns, "{}/handler".format(task_path), partial(nsGet(ns, "/blocks/echo/handler"), task_path))
    nsSet(ns, "{}/call".format(task_path), partial(nsGet(ns, "/blocks/echo/call"), task_path))
    nsDaemon(ns, "TASK:echo:{}".format(name), nsGet(ns, "{}/server".format(task_path)))
    return True

def nsBlockEchoIn(ns, block_path, task_path, data):
    nsSet(ns, "{}/data".format(task_path), data)
    return True

def nsBlockEchoOut(ns, block_path, task_path):
    return nsGet(ns, "{}/data".format(task_path))

def nsBlockEchoServer(ns, block_path, task_path):
    return

def nsBlockEchoExists(ns, block_path, name):
    return name in nsDir(ns, "/tasks/echo")


_mkdir = [
    "/usr/local/blocks/echo",
    "/blocks/echo",
    "/tasks/echo",
]

_lib = {
    "/usr/local/blocks/echo/init" : nsBlockEchoInit,
    "/usr/local/blocks/echo/task": nsBlockEchoTask,
    "/usr/local/blocks/echo/in": nsBlockEchoIn,
    "/usr/local/blocks/echo/out": nsBlockEchoOut,
    "/usr/local/blocks/echo/server": nsBlockNullServer,
    "/usr/local/blocks/echo/handler": nsBlockNullHandler,
    "/usr/local/blocks/echo/call": nsBlockNullCall,
    "/usr/local/blocks/echo/exists": nsBlockEchoExists,
    "/usr/local/blocks/echo/running": nsBlockEchoExists,
}
