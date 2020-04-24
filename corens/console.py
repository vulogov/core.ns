import gevent
import time
import json
from Cheetah.Template import Template
from clint.textui import indent, puts, colored
from corens.ns import nsGet
from corens.txt import nsTxt


def nsConsole(ns,  *msg, **kw):
    if nsGet(ns, "/etc/console") is False:
        return msg
    q = nsGet(ns, "/sys/console")
    for _m in msg:
        _m = str(_m)
        _msg = _m % kw
        _msg = nsTxt(ns, _msg)
        q.put_nowait(_msg)
    return msg

def nsConsolePush(ns, *msg):
    if nsGet(ns, "/etc/console") is False:
        return msg
    q = nsGet(ns, "/sys/console")
    for _m in msg:
        q.put_nowait(_m)


def nsconsole(ns, *msg, **kw):
    if nsGet(ns, "/etc/console") is False:
        return msg
    for _m in msg:
        _m = str(_m)
        _msg = _m % kw
        _msg = nsTxt(ns, _msg)
        try:
            with indent(4, quote=colored.green("|")):
                puts(_msg)
        except ValueError:
            return

def nsConsoleProcess(ns, entries=1):
    q = nsGet(ns, "/sys/console")
    c = 0
    while True:
        if q.qsize() > 0:
            msg = q.get_nowait()
            c += 1
        else:
            break
        if isinstance(msg, str) is True:
            with indent(4, quote=colored.green("|")):
                puts(msg)
        elif isinstance(msg, dict) is True and "dir" not in msg:
            nsConsoleLogWrite(ns, msg)
        elif isinstance(msg, dict) is True and "dir" in msg:
            with indent(4, quote=colored.magenta(msg["dir"])):
                del msg["dir"]
                puts(json.dumps(msg))
        else:
            with indent(4, quote=colored.cyan("|")):
                puts(str(msg))
        if c >= entries:
            break
        gevent.sleep(nsGet(ns, "/etc/consoleInBatchDelay", 0.5))

def nsConsoleDaemon(ns):
    while True:
        nsConsoleProcess(ns, nsGet(ns, "/etc/consoleBatchSize", 10))
        gevent.sleep(nsGet(ns, "/etc/consoleAfterBatchDelay", 3))

def nsConsoleSize(ns):
    q = nsGet(ns, "/sys/console")
    return q.qsize()

def nsConsoleLogWrite(ns, msg):
    if nsGet(ns, "/etc/logConsoleAsJSON", False) is True:
        print(json.dumps(msg))
        return
    level_m = ["DBG", "INF", "WRN", "ERR", "CRT", "PNC"]
    level_c = [colored.white, colored.green, colored.cyan,
    colored.yellow, colored.red, colored.magenta]
    print(level_c[msg['level']](level_m[msg['level']]),
        colored.white(time.strftime("[%m/%d %H:%M:%S]", time.localtime(msg['stamp']))),
        colored.yellow(msg['msg']))
    if msg['level'] == 5:
        nsConsole(ns, "DON'T PANIC !")
    return
