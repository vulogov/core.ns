import time
import uuid
import gevent
from corens.txt import nsTxt
from corens.ns import nsGlobalError, nsGet, nsLs, nsSet

LOG_LEVELS=['debug', 'info', 'warning', 'error', 'critical', 'panic']

def nsLogInit(ns, *args, **kw):
    nsSet(ns, "/etc/logToConsole", True)
    return

def nsLog(ns, lvl, msg, **kw):
    if nsGet(ns, "/etc/log") is False:
        return None
    out = {'level': lvl, 'msg': msg % kw, 'id':str(uuid.uuid4()), 'stamp': time.time()}
    out['msg'] = nsTxt(ns, out['msg'])
    q = nsGet(ns, "/sys/log/messages")
    q.put_nowait(out)
    if lvl >=4:
        nsGlobalError(ns, out)
    return out

def nsDebug(ns, msg, **kw):
    return nsLog(ns, 0, msg, **kw)

def nsInfo(ns, msg, **kw):
    return nsLog(ns, 1, msg, **kw)

def nsWarning(ns, msg, **kw):
    return nsLog(ns, 2, msg, **kw)

def nsError(ns, msg, **kw):
    return nsLog(ns, 3, msg, **kw)

def nsCritical(ns, msg, **kw):
    return nsLog(ns, 4, msg, **kw)

def nsPanic(ns, msg, **kw):
    return nsLog(ns, 5, msg, **kw)

def nsLogProcess(ns, entries=1):
    q = nsGet(ns, "/sys/log/messages")
    logs = nsLs(ns, "/sys/log/channels")
    c = 0
    while True:
        if q.qsize() > 0:
            msg = q.get_nowait()
            c += 1
        else:
            break
        for log in logs:
            logs[log](msg)
        if c >= entries:
            break
        gevent.sleep(nsGet(ns, "/etc/logInBatchDelay", 0.5))

def nsLogToConsole(ns, msg):
    if nsGet(ns, "/etc/console") is False:
        return
    q = nsGet(ns, "/sys/console")
    q.put_nowait(msg)


def nsLogDaemon(ns):
    while True:
        nsLogProcess(ns, nsGet(ns, "/etc/logBatchSize", 10))
        gevent.sleep(nsGet(ns, "/etc/logAfterBatchDelay", 3))

def nsLogSize(ns, entries=1):
    q = nsGet(ns, "/sys/log/messages")
    return q.qsize()
