from corens.ns import *

def nsCookie(ns, cookie):
    return cookie == nsGet(ns, "/security/cookie")
