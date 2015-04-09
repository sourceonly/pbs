#!/usr/bin/python

import time
import os
import sys

script=sys.argv[0]
title = ""
if os.environ.has_key('PAS_ACTION_TITLE'):
    title=os.environ['PAS_ACTION_TITLE']
else:
    print "error: expected PAS_ACTION_TITLE variable not found"
    exit(106)

print "Executing script: " + script + " with title : " + title
sys.stdout.flush()
