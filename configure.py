# Original python 2 code:
"""
import commands

# Create path.rtk
status, abs_path = commands.getstatusoutput("pwd")
f = open("path.rkt", "w")
f.write("#lang racket\n")
f.write("(provide (all-defined-out))\n")
f.write("(define srcpath \"" + abs_path + "\")\n")
print "path.rkt is created."
"""

from pathlib import Path

abs_path = str(Path('.').absolute())
with open("path.rkt", "w") as f:
    f.write("#lang racket\n")
    f.write("(provide (all-defined-out))\n")
    f.write("(define srcpath \"" + abs_path + "\")\n")
    print("path.rkt is created.")
