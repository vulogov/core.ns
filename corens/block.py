import gevent
from corens.ns import *

def nsBlockNullHandler(ns, block_path, task_path,  data,  *args, **kw):
    return data

def nsBlockNullServer(ns, block_path, task_path):
    return

def nsBlockNullCall(ns, block_path, task_path, data, *args, **kw):
    nsSet(ns, "{}/args".format(task_path), args)
    nsSet(ns, "{}/kw".format(task_path), kw)
    nsGet(ns, "{}/in".format(task_path))(data)


def nsBlockLoopSimple(ns, block_path, task_path, *args):
    in_fun = nsGet(ns, "{}/inF".format(task_path))
    out_fun = nsGet(ns, "{}/outF".format(task_path))
    while True:
        data = None
        if in_fun is not None:
            data = in_fun()
        if data is not None:
            h_fun = nsGet(ns, "{}/handler".format(task_path))
            args = nsGet(ns, "{}/args".format(task_path), ())
            kw = nsGet(ns, "{}/kw".format(task_path), {})
            data = h_fun(data, *args, **kw)
        if data is not None:
            out_fun(data)
        delay = nsGet(ns, "{}/sleep".format(task_path), nsGet(ns, "/etc/defaultTaskLoopSleep"))
        gevent.sleep(delay)
