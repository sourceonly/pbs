#!/usr/bin/python
#
# (c) Copyright 2010 Altair Engineering, Inc.  All rights reserved.
#
# This code is provided as is without any warranty, express or implied,
# or indemnification of any kind.
# All other terms and conditions are as specified in the Altair PBS EULA.
#

# TO DO:
# - Add error handling to file opening and reading
# - Use a single regexp with multiple clauses
#

import time
import os
import sys
import time
import re

print os.environ['PBS_JOBID']
print os.environ['PBS_JOBDIR']
os.chdir(os.environ['PBS_JOBDIR'])

f=open('currentEngineFile','r')
currentEngineFile=f.readline()
f.close()

#
# Determine Radioss input format and signal file name
regexp_v5_fmt = re.compile('(?P<engineName>.*)_(?P<nmb>\d\d\d\d)\.rad$')
regexp_v4_fmt = re.compile('(?P<engineName>.*)D(?P<nmb>\d\d)$')
if regexp_v5_fmt.search(currentEngineFile):
  #
  # It's a v5 run
  print "Action Terminate: Radioss input file version 5."
  result=regexp_v5_fmt.search(currentEngineFile)
  engineName=result.group('engineName')
  engineNumber=result.group('nmb')
  engineVersion=5
  stopFile=engineName + "_" + engineNumber + ".ctl"
  messageFile=engineName + "_" + engineNumber + ".lis"
elif regexp_v4_fmt.search(currentEngineFile):
  #
  # It's a v4 run
  print "Action Terminate: Radioss input file version 4."
  result=regexp_v4_fmt.search(currentEngineFile)
  engineName=result.group('engineName')
  engineNumber=result.group('nmb')
  engineVersion=4
  stopFile=engineName + "C" + engineNumber
  messageFile=engineName + "L" + engineNumber
else:
  #
  # Unknown format
  print "Action Terminate: Unknown Radioss input file version. Exiting."
  sys.exit()

#
# Create signal file
f=open(stopFile,'w')
f.write("/STOP\n")
f.close()

#
# Wait for Radioss to finish
regexp_termination=re.compile('T E R M I N A T I O N')
f=open(messageFile,'r')
while 1:
  where = f.tell()
  line = f.readline()
  if not line:
    time.sleep(1)
    f.seek(where)
  else:
    if regexp_termination.search(line):
      print "Action Terminate: Radioss temrination detected."
      break
f.close()


sys.stdout.flush()
