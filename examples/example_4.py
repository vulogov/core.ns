import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *
from corens.mod import lf

def log_JSON(ns):
    time.sleep(10)
    f = lf(ns)
    f("V")("/etc/logConsoleAsJSON", True)
    f("/bin/info")("Test of info log message as JSON")


ns, f, F = NS()
print("This program will demo the output of the log entries in various formats on console")
print("Wait few seconds for a JSON messages. Yes, you can dynamically change Text/JSON")
f("schedule")(10, "JSON", log_JSON)
f("/bin/debug")("Test of debug log message")
f("/bin/info")("Test of info log message")
f("/bin/warning")("Test of warning log message")
f("/bin/error")("Test of error log message")
f("/bin/critical")("Test of critical log message")
f("/bin/panic")("Test of panic log message")
f("/sbin/loop")()
