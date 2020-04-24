import pyfiglet
from texttable import Texttable
from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsBannerStart(ns, *args, **kw):
    if nsGet(ns, "/etc/flags/banner", False) is True:
        pyfiglet.print_figlet(
            nsGet(ns, "/etc/name"),
            nsGet(ns, "/etc/bannerFont", "isometric2"),
            "GREEN:"
        )
        tbl = Texttable(nsGet(ns, "/etc/bannerTableWidth", 120))
        tbl.set_deco(Texttable.HEADER)
        tbl.add_rows(
            [
                ["Variable", "Value", "Description"],
                ["/etc/name", nsGet(ns, "/etc/name"), "Name of the application"],
                ["/etc/hostname", nsGet(ns, "/etc/hostname"), "Hostname"],
                ["/sys/env/platform/platform", nsGet(ns, "/sys/env/platform/platform"), "Host platform"],
                ["/sys/env/platform/python", nsGet(ns, "/sys/env/platform/python"), "Version of the Python"],
                ["/sys/env/platform/system", nsGet(ns, "/sys/env/platform/system"), "OS Name"],
                ["/sys/env/user", nsGet(ns, "/sys/env/user"), "Name of the user"],
                ["/sys/env/home", nsGet(ns, "/sys/env/home"), "Home directory"],
                ["/sys/env/apphome", nsGet(ns, "/sys/env/apphome"), "Application home"],
                ["/sys/env/pidFile", nsGet(ns, "/sys/env/pidFile"), "PID file"],
                ["/sys/env/apphome", nsGet(ns, "/sys/env/apphome"), "Application home"],
                ["/config/user.library", nsGet(ns, "/config/user.library"), "Application library"],
                ["/etc/daemonize", nsGet(ns, "/etc/daemonize"), "Become daemon ?"],
                ["/etc/flags/internalServer",nsGet(ns, "/etc/flags/internalServer", False),"Enable internal server"],
                ["/etc/version", str(nsGet(ns, "/etc/version")), "Application version"],
                ["/etc/release", nsGet(ns, "/etc/release"), "Application release"],
                ["/etc/author", nsGet(ns, "/etc/author"), "Author of application"],
                ["/etc/author.email", nsGet(ns, "/etc/author.email"), "Author's email"],
                ["/etc/corens/version", str(nsGet(ns, "/etc/corens/version")), "core.NS version"],
                ["/etc/corens/release", nsGet(ns, "/etc/corens/release"), "core.NS release"],
                ["/config/RPCCatchCalls", nsGet(ns, "/config/RPCCatchCalls"), "Trace RPC"],
                ["/config/answer", nsGet(ns, "/config/answer"), "THE ANSWER"],
            ]
        )
        print(tbl.draw())


def nsBannerStop(ns, *args, **kw):
    if nsGet(ns, "/etc/flags/banner", False) is True:
        pyfiglet.print_figlet(
            nsGet(ns, "/etc/byeMsg", "DON'T PANIC!"),
            nsGet(ns, "/etc/byeMsgFont", "ogre"),
            "RED:"
        )

_init = [
    "0banner"
]

_actions = {
    "0banner": {
        "start" : nsBannerStart,
        "stop" : nsBannerStop
    }
}
