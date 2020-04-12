import time
from corens import *

def answer(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    V("/tmp/answer", 42)

def killer5(*args):
    print("Hi from killer5")
    f = lf(args[0])
    c = 0
    while True:
        print(c,f("/bin/sps")())
        c += 1
        time.sleep(1)
        if c > 5:
            break
    f("/sbin/killall")()

print("Let's start")
ns, f, F = NS()
print("Env created")
f("spawn")("killer", killer5)
print("Entering the loop")
f("schedule")(1, "42", answer)
f("/sbin/loop")()
print(f("V")("/tmp/answer"))
