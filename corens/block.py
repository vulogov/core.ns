import gevent
from corens.ns import *

def nsBlockQueueGet(ns, block_path, task_path, _queue_path):
    q = nsGet(ns, _queue_path)
    if q is None:
        return None
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is True:
        return q.get()
    if q is None or len(q) == 0 and nsGet(ns, "{}/blocking".format(task_path)) is False:
        return None
    return q.get_nowait()

def nsBlockNullHandler(ns, block_path, task_path,  data,  *args, **kw):
    return data

def nsBlockNullTrue(ns, block_path, task_path,  data,  *args, **kw):
    return True


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

def nsBlockLoopEmit(ns, block_path, task_path, *args):
    out_fun = nsGet(ns, "{}/outF".format(task_path))
    h_fun = nsGet(ns, "{}/handler".format(task_path))
    while True:
        data = None
        if h_fun is not None:
            args = nsGet(ns, "{}/args".format(task_path), ())
            kw = nsGet(ns, "{}/kw".format(task_path), {})
            data = h_fun(data, *args, **kw)
            if data is not None:
                out_fun(data)
        delay = nsGet(ns, "{}/sleep".format(task_path), nsGet(ns, "/etc/defaultTaskLoopSleep"))
        gevent.sleep(delay)

def nsBlockLoopFilter(ns, block_path, task_path, *args):
    in_fun = nsGet(ns, "{}/inF".format(task_path))
    out_fun = nsGet(ns, "{}/outF".format(task_path))
    r_fun = nsGet(ns, "{}/reject".format(task_path))
    while True:
        data = None
        if in_fun is not None:
            data = in_fun()
        if data is not None:
            h_fun = nsGet(ns, "{}/handler".format(task_path))
            args = nsGet(ns, "{}/args".format(task_path), ())
            kw = nsGet(ns, "{}/kw".format(task_path), {})
            if h_fun(data, *args, **kw) is False:
                if r_fun is not None:
                    r_fun(data, *args, **kw)
                data = None
        if data is not None:
            out_fun(data)
        delay = nsGet(ns, "{}/sleep".format(task_path), nsGet(ns, "/etc/defaultTaskLoopSleep"))
        gevent.sleep(delay)

def nsBlockLoopGate(ns, block_path, task_path, *args):
    in_fun = nsGet(ns, "{}/inF".format(task_path))
    out_fun = nsGet(ns, "{}/outF".format(task_path))
    while True:
        data = None
        gate = nsGet(ns, "{}/gate".format(task_path))
        if gate is True:
            if in_fun is not None:
                data = in_fun()
            if data is not None:
                out_fun(data)
        delay = nsGet(ns, "{}/sleep".format(task_path), nsGet(ns, "/etc/defaultTaskLoopSleep"))
        gevent.sleep(delay)
