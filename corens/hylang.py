from corens.ns import nsMkdir, nsSet, nsGet, nsGlobalError, nsLs
from hy import read_str, eval

def nsImportPfun(ns, env, *vpath):
    for p in vpath:
        env.update(nsLs(ns, p))
    return env


def nsHYmkenv(ns, **kw):
    env = globals()
    env["nsGet"] = nsGet
    env["nsSet"] = nsSet
    env["f"] = nsGet(ns, "/bin/f")
    env["ns"] = ns
    return env

def nsHYInit(ns, *args, **kw):
    env = nsHYmkenv(ns, **kw)
    nsMkdir(ns, "/pbin")
    nsMkdir(ns, "/psbin")
    nsSet(ns, "/sys/hylang.enabled", False)
    nsHyEval(ns, '(nsSet ns "/sys/hylang.enabled" True)')

def nsHyEval(ns, expression):
    env = nsHYmkenv(ns)
    env = nsImportPfun(ns, env, "/psbin", "/pbin")
    try:
        _expr = read_str(str(expression))
        _res = eval(_expr, env)
    except Exception as e:
        nsGlobalError(ns, "{}".format(e))
        return None
    return _res

def nsHyPipeline(ns, expression):
    _exp = u"""(->
    {})""".format(expression)
    return nsHyEval(ns, _exp)
