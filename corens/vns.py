import time
import uuid
import os.path
from toolz import partial
from corens.ns import *
import vedis

def nsVNSinit(ns):
    return ns

def nsVopen(ns, name, path=':mem:', **kw):
    if path != ':mem:':
        path = os.path.abspath(path)
        if not os.path.exists(path) or not os.path.isfile(path):
            return None
    dev_path = kw.get("target", None)
    if dev_path is None:
        dev_path = nsGet(ns, "/config/dev/path", "/dev")
    _path = "{}/{}".format(dev_path, name)
    ctx = nsMkdir(ns, _path)
    v = vedis.Vedis(path)
    nsSet(ns, "{}/image".format(_path), v)
    nsSet(ns, "{}/stamp".format(_path), time.time())
    nsSet(ns, "{}/id".format(_path), str(uuid.uuid4()))
