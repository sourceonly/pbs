#!/usr/bin/python

import time
import os
import sys

script=sys.argv[0]
signal = ""
if os.environ.has_key('PAS_ACTION_SIGNAL'):
    signal=os.environ['PAS_ACTION_SIGNAL']
else:
    print "error: expected PAS_ACTION_SIGNAL variable not found"
    exit(106)

print "Executing script: " + script + " with signal : " + signal
f = open(signal, "w+b")
f.close
sys.stdout.flush()
