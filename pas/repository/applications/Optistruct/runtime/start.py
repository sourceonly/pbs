#!/usr/bin/python

import time
import os
import sys
#import shutil

#shutil.copyfile("runtime/Template1.tplt","Template1.tplt");
#shutil.copyfile("runtime/Template2.tani","Template1.tani");


our_os = os.uname()[0]
arch = os.uname()[4]
input_file = os.path.basename(os.environ['MASTER'])
opti_ver=(os.environ['PAS_VERSION'])
extra_args = ""
cwd = os.getcwd()

# Create the extra arguments string
extra_args = " ".join([arg.strip for arg in sys.argv[1:]])


# Set up environment variables
os.environ['TMPDIR'] = cwd

# Assemble the command
cmd = "%s -len %s -cpu %s %s %s" % ( os.environ['PAS_EXECUTABLE'], 
	os.environ['MEM'], os.environ['TOTAL_NCPUS'], input_file, extra_args )
   
#set license server
#if (opti_ver == "12.0" ):
os.environ['ALTAIR_LICENSE_PATH'] = '6200@gn01'
#elif (opti_ver == "11.0" ):
#	os.environ['ALTAIR_LICENSE_PATH'] = '6200@192.168.40.66'

 
#set optistruct temp directory to use PBS-managed 'TMPDIR"
os.environ['TEMP'] = os.environ['TMPDIR']

print >>sys.stderr, "Environment Dump:\n%s " % "\n".join( 
	"%s => %s" % (i, os.environ[i]) for i in os.environ )

print "Executing command: "+cmd
sys.stdout.flush()
sys.stderr.flush()

#run application
rc=os.system (cmd)
os.system("./runtime/create_report")
os.system("/bin/sleep 100")
sys.exit(rc)
