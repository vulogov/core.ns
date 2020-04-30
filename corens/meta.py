from corens.ns import *
from textx import metamodel_from_str
import textx.exceptions

def nsMeta(ns, path, model):
    mm = nsGet(ns, path)
    if mm is None:
        return
    return mm.model_from_str(model)
