import os
import os.path
from corens.console import nsconsole
from corens.ns import *
from corens.zmq import *

def nsSecurityStart(ns, *args, **kw):
    nsconsole(ns, "Setting up security")
    nsMkdir(ns, "/security")
    nsSet(ns, "/security/cookie", str(uuid.uuid4()))
    apphome = nsGet(ns, "/sys/env/apphome")
    with open("{}/cookie".format(apphome), "w") as f:
        f.write(nsGet(ns, "/security/cookie"))
    return


def nsSecurityStop(ns, *args, **kw):
    nsconsole(ns, "Cleaning up security")
    apphome = nsGet(ns, "/sys/env/apphome")
    cookie_path = "{}/cookie".format(apphome)
    if os.path.exists(cookie_path) is True and os.path.isfile(cookie_path) is True:
        os.unlink(cookie_path)
    return

_init = [
    "0security"
]

_actions = {
    "0security": {
        "start" : nsSecurityStart,
        "stop" : nsSecurityStop
    }
}
