#!/usr/bin/python

import time
import os
import sys

script=sys.argv[0]
sys.argv.pop(0)
print "Executing script " + script + " of application optistruct\n"
sys.stdout.flush()

# dummy implementation. Comment it out if needed
seconds = os.environ['PAS_MEM']

print "arguments:"
for a in sys.argv:
    print a + ' '
print ' '

print "start.py environment:"
for a in os.environ.keys():
    var = a + '=' + os.environ[a]
    print var
print 

print "current directory contents:"
filenames = os.listdir(os.curdir)      
for filename in filenames:
    print filename
print 

sys.stdout.flush()

os.system('qstat -f ' + os.environ['PBS_JOBID'])

print "PAS job sleeping for " + seconds + " seconds"
time.sleep(int(seconds))


##real implementation
#PAS_EXECUTABLE = os.environ['PAS_EXECUTABLE']
#cmd = PAS_EXECUTABLE
#for a in sys.argv:
#   cmd += ' ' + a
#   
##set license server
#os.environ['PAS_LICENSE_FILE'] = os.environ['PAS_LIC_GRIDWORKS']
# 
##set optistruct temp directory to use PBS-managed 'TMPDIR"
#os.environ['TEMP'] = os.environ['TMPDIR']
#
##run application
#os.system (cmd)
