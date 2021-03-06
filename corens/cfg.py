from fs.opener import open_fs
from fs.errors import CreateFailed
from corens.ns import *
from corens.cfg_grammar import nsCfgGrammar
from corens.version import *

def nsDefaults(ns):
    nsSet(ns, "/config/var.redefine", True)
    nsSet(ns, "/config/cmd.run", False)
    nsSet(ns, "/config/path", ["/home", "/bin", "/sbin"])
    nsSet(ns, "/config/dev.path", "/dev")
    nsSet(ns, "/config/cfg.path", ['osfs://.','osfs://tests'])
    nsSet(ns, "/config/cfg.fs", {})
    nsSet(ns, "/config/cfg.files", [])
    nsSet(ns, "/config/library", ["corens.stdlib"])
    nsSet(ns, "/config/user.library", [])
    nsSet(ns, "/config/cmd.path", "/usr/local/bin")
    nsSet(ns, "/config/cmd.kw", {})
    nsSet(ns, "/config/answer", 42)
    nsMkdir(ns, "/etc/corens")
    nsSet(ns, "/etc/corens/version", VERSION)
    nsSet(ns, "/etc/corens/release", RELEASE)
    nsSet(ns, "/etc/corens/url", URL)
    nsSet(ns, "/etc/corens/author", AUTHOR)
    nsSet(ns, "/etc/corens/author.email", AUTHOR_EMAIL)
    nsSet(ns, "/etc/corens/license", LICENSE)
    nsSet(ns, "/etc/version", "0.0")
    nsSet(ns, "/etc/release", "0.0.0")
    nsSet(ns, "/etc/author", "Unknown")
    nsSet(ns, "/etc/author.email", "Unknown@Example.com")
    nsSet(ns, "/etc/license", "GPL3")
    nsSet(ns, "/etc/url", "http://www.example.com")
    nsSet(ns, "/etc/shell.prompt", " #  ")
    nsSet(ns, "/etc/daemonize", False)
    nsSet(ns, "/etc/singleCopy", False)
    nsSet(ns, "/etc/listen", {})
    nsSet(ns, "/etc/rpc", {})
    # Metaprogramming, blocks and pipelines
    nsMkdir(ns, "/etc/meta")
    nsMkdir(ns, "/meta")
    nsMkdir(ns, "/metaprocessor")
    nsSet(ns, "/etc/defaultTaskLoopSleep", 0)
    nsMkdir(ns, "/tasks")
    nsMkdir(ns, "/blocks")
    nsMkdir(ns, "/pipelines")
    # Console and log configuration
    nsSet(ns, "/etc/consoleInBatchDelay", 0.5)
    nsSet(ns, "/etc/consoleAfterBatchDelay", 3)
    nsSet(ns, "/etc/consoleBatchSize", 10)
    nsSet(ns, "/etc/consoleEmitter", "tcp://127.0.0.1:61111")
    nsSet(ns, "/etc/logInBatchDelay", 0)
    nsSet(ns, "/etc/logAfterBatchDelay", 3)
    nsSet(ns, "/etc/logBatchSize", 10)
    # RPC
    nsSet(ns, "/config/defaultRPCListen", "127.0.0.1")
    nsSet(ns, "/config/defaultInternalListen", "127.0.0.1")
    nsSet(ns, "/config/defaultInternalPort", 61000)
    nsSet(ns, "/config/defaultInternalMax", 10)
    nsSet(ns, "/config/RPCCatchCalls", False)
    #
    nsSet(ns, "/etc/shutdownRequested", False)

    for c in nsGet(ns, "/config/cfg.path"):
        nsCfgAppendFs(ns, c)
    ns = nsCfgGrammar(ns)
    return ns

def nsCfgAppendFs(ns, fsname):
    cfg_fs = nsGet(ns, "/config/cfg.fs")
    if fsname not in cfg_fs:
        try:
            nsGet(ns, "/config/cfg.fs")[fsname] = open_fs(fsname)
        except CreateFailed:
            return None
    return nsGet(ns, "/config/cfg.fs")[fsname]

def nsCfgListenParse(ns, listenspec):
    try:
        ix  = listenspec.index('@')
        return listenspec[:ix], listenspec[ix+1:]
    except ValueError:
        return listenspec, listenspec
