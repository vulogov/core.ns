import sys
import re
import clint
from corens.ns import *
from corens.help import *
from corens.mod import f

def nsArgs(ns, args=sys.argv[1:]):
    path = "/etc/args"
    nsSet(ns, "/etc/argv", [])
    argv = nsGet(ns, "/etc/argv")
    _args = nsGet(ns, path)
    args = clint.arguments.Args(args, True)
    _path = "{}/default".format(path)
    nsMkdir(ns, path)
    isFlag = False
    prev = None
    while True:
        a = args.pop(0)
        if a is None or isinstance(a, str) is not True:
            break
        if len(a) == 0:
            continue
        if re.match(r'--help', a) is not None:
            if prev is None:
                hpath = "/help/cmd/default"
            else:
                hpath = "/help/cmd/{}".format(prev)
            nsHelp(ns, hpath)
            raise SystemExit
        if re.match(r'--(.*)', a) is not None and isFlag is False:
            isFlag = True
            prev = a[2:]
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), True)
            isFlag = True
            prev = a[2:]
            continue
        if re.match(r'--(.*)', a) is None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), a)
            isFlag = False
            continue
        if re.match(r'--(.*)', a) is None and isFlag is False:
            prev = a
            argv.append(a)
            _path = "{}/{}".format(path, a)
            nsMkdir(ns, _path)
            continue
    return ns

def nsCmd(ns, *args, **kw):
    argv = nsGet(ns, "/etc/argv", [])
    root = nsGet(ns, "/config/cmd.path")
    kw.update(nsGet(ns, "/config/cmd.kw"))
    out = None
    for k in argv:
        _args = tuple([out,] + list(args))
        out = f(ns, "{}/{}".format(root, k))(*_args, **kw)
    return ns
