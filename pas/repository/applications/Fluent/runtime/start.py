#!/usr/bin/python
#
# (c) Copyright 2012 Altair Engineering, Inc.  All rights reserved.
# modified by:   ESG Team, Bangalore India 
# This code is provided as is without any warranty, express or implied,
# or indemnification of any kind.
# All other terms and conditions are as specified in the Altair PBS EULA.
#

import time
import os
import sys

##### Debug output
def debug_output():
        #list env
        print "Start.py environment:"
        for a in sorted(os.environ) :
            var = a + '=' + os.environ[a]
            print var
        print

        #list files in current directory
        print 'Contents of ' + os.getcwd() + ':'
        topleveldir_listing = os.listdir(os.getcwd())
        # todo: add a check that there are too many files in some directory and truncate output
        iteration_rc = 0;
        for a in sorted(topleveldir_listing):
            print a
        print

        sys.stdout.flush()




##### Debug output switch
debugOn=0
if ( 'STARTPY_DEBUG' in os.environ ) :
  debugOn=int(os.environ['STARTPY_DEBUG'])

if (debugOn):
        debug_output()


os.environ['TEMP']=os.environ['TMPDIR']

MPI_TYPE=os.environ['MPI_TYPE'].lower()
print MPI_TYPE ; sys.stdout.flush()
if ( MPI_TYPE == "hpmpi" ):
  # Set up environment for HP-MPI
  del os.environ['OMP_NUM_THREADS']
  mpi_code='hp'
elif ( MPI_TYPE == "intelmpi" ):
  # Set up environment for IntelMPI
  print "MPI type: IntelMPI"
elif ( MPI_TYPE == "openmpi" ):
  # Set up environment for OpenMPI
  print "MPI type: OpenMPI"
elif ( MPI_TYPE == "mpich" ):
  # Set up environment for MPICH
  print "MPI type: MPICH"
elif ( MPI_TYPE == "lammpi" ):
  # Set up environment for LamMPI
  print "MPI type: LamMPI"
else:
  # SMP run chosen
  print "MPI type: NONE (SMP run)"
  mpi_code="none"

if ( os.environ['PRECISION'].lower() == 'double' ):
  PRECISION='dp'
else:
  PRECISION=''

if sys.platform == 'win32':
   import win32api
AIF_EXECUTABLE = os.environ['AIF_EXECUTABLE'] 
if sys.platform == 'win32':
   AIF_EXECUTABLE = win32api.GetShortPathName(AIF_EXECUTABLE);
sys.argv.pop(0) 
display=os.environ['AIF_DISPLAY']
cmd ='export DISPLAY='+display + ':0.0;export FLUENT_ARCH=lnamd64;'
#cmd ='export FLUENT_ARCH=lnamd64;'
cmd += 'export LM_LICENSE_FILE=1055@cn0:/ansys_inc/shared_files/licensing/license.dat; ' + AIF_EXECUTABLE 


cmd += ' ' + os.environ['DIMENSION'] + PRECISION
#cmd += ' -r' + os.environ['AIF_VERSION']
#cmd += ' -r6.3.26 '
if  os.environ['AIF_VERSION']=='GUI':
   cmd+=' -i '
   cmd += ' -r6.3.26 '
else: 
   cmd+=' -r13.0.0 -i'
#   cmd+=' -r13.0.0 '
print 'version is 13.0.0 : ' + cmd
if ( 'INTERACTIVE' in os.environ ):
  if (len(os.environ['INTERACTIVE']) > 0 ):
    cmd += ' ' + os.environ['INTERACTIVE']
if mpi_code == 'none':
  # SMP run
  cmd = AIF_EXECUTABLE
else:
  # MPI RUN
  cmd += ' -t' + os.environ['CORES']
  cmd += ' -ssh'
  cmd += ' -mpi=' + mpi_code
  cmd += ' -cnf=' + os.environ['PBS_NODEFILE']

if ( 'JOURNAL' in os.environ ):
  cmd += ' -i ' +  os.environ['JOURNAL']

cmd += ' > ' + os.environ['PBS_JOBNAME'] + '.log'

#run application 
print cmd 
os.system (cmd)
sys.stdout.flush()
