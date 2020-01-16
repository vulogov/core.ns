import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from corens import *
ns, f, F = NS()
V = f("V")
C = f("C")
C('[ /home > Answer <- 42 List <- [1,2,3] { answer: 42} -> D Pi <- 3.14 ;;' )
print(V("/home/Answer"))
print(V("/home/List"))
print(V("/home/D"))
print(V("/home/Pi"))
