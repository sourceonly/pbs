#!/usr/bin/python
#
# (c) Copyright 2010 Altair Engineering, Inc.  All rights reserved.
#
# This code is provided as is without any warranty, express or implied,
# or indemnification of any kind.
# All other terms and conditions are as specified in the Altair PBS EULA.
#


# TO DO:
# - add SMP executable support through the use of PBS App Svcs booleans
# - add support for multiple executable architecture and not only "p4linux964"
#   and make them choosen from interface and influencing submission (-> presubmit.py)
# - Fetch executables paths from site-config.xml


import time
import os
import sys
import re

##### Debug output
def debug_output():
        #list env
        print "\n\nstart.py environment:"
        for a in os.environ.keys():
            var = a + '=' + os.environ[a]
            print var
        print
        #list files
        os.system('ls -la')
        sys.stdout.flush()


##### Debug output switch
debugOn=1

if (debugOn):
        debug_output()

##### Set up environment fo RADIOSS
#os.environ['ALTAIR_LM_LICENSE_FILE']=os.environ['PAS_LIC_GRIDWORKS']
os.environ['TEMP']=os.environ['TMPDIR']
hosts=int(os.environ['PAS_HOSTS'])
cores=int(os.environ['PAS_CORES'])
os.environ['TOTALNCPUS']=str(hosts * cores)   
print "TOTALNCPUS" + os.environ['TOTALNCPUS']

MPI_TYPE=os.environ['MPI_TYPE'].lower()
print MPI_TYPE ; sys.stdout.flush()
if ( MPI_TYPE == "hpmpi" ):
  # Set up environment for HP-MPI
  del os.environ['OMP_NUM_THREADS']
  del os.environ['NCPUS']
  os.environ['MPI_ROOT']="/opt/plmpi"
  os.environ['PROTO']="TCP"
  os.environ['MPI_REMSH']="/usr/bin/rsh"
  os.environ['P4_RSHCOMMAND']=os.environ['MPI_REMSH']
  os.environ['PBS_RSHCOMMAND']="/usr/bin/rsh"
  os.environ['MPI_CPU_AFFINITY']="ll"
  os.environ['LD_LIBRARY_PATH']="/hosts/node007/data02/Logiciels/ALTAIR/hw12.0/altair/hwsolvers/common/bin/linux64"
  os.environ['PATH']="%s%s%s" % (os.environ['MPI_ROOT'], ":", os.environ['PATH'])
  radioss_mpi_code="hp"
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

##### Set up executables name based on version number
os.environ['RADIR']="/hosts/node007/data02/Logiciels/ALTAIR/hw12.0/altair/hwsolvers/radioss/bin/linux64"
#radioss_ver=os.path.basename(os.environ['PAS_EXECUTABLE']).split('_',1)[0]
#radioss_ver=radioss_ver[1:]
#radioss_arc=os.path.basename(os.environ['PAS_EXECUTABLE']).split('_',1)[1]

pas_version=(os.environ['PAS_VERSION'])
#starterbin=os.path.basename(os.environ['PAS_EXECUTABLE'])
#enginebin="e_" + pas_version + '_linux64_plmpi'
enginebin=os.environ['PAS_EXECUTABLE']
starterbin="s_12.0.210_linux64"
#print radioss_ver
#starterbin="s_11.0_linux64"
#enginebin="e_11.0_linux64_plmpi"

##### Copy license client executable to local directory
#copy_cmd="%s %s/%s %s" % ("cp", os.environ['RADIR'], "radflex9_linux", ".")
#print copy_cmd
#os.system(copy_cmd)
#copy_cmd="%s %s/%s %s" % ("cp", os.environ['RADIR'], "radflex10_linux", ".")
#print copy_cmd
#os.system(copy_cmd)
copy_cmd="%s %s/%s %s" % ("cp", os.environ['LD_LIBRARY_PATH'], "radflex_12_linux64", ".")
print copy_cmd
os.system(copy_cmd)

cleanup_cmd="rm -f ./radflex_12_linux64"
#cleanup_cmd=cleanup_cmd + " ./radflex_11_linux64"

if ( os.environ['RUNTYPE'] == "starter" ) or ( os.environ['RUNTYPE'] == "both" ):
        starterName=os.path.basename(os.environ['STARTERFILE'])
        if len(starterName) == 0:
                print "Starter run requested but starter file is not specified: skipping starter."
        else:
                #
                # Determine Radioss input format and signal file name
                regexp_v5_fmt = re.compile('(?P<starterName>.*)_(?P<nmb>\d\d\d\d)\.rad$')
                regexp_v4_fmt = re.compile('(?P<starterName>.*)D(?P<nmb>\d\d)$')
                if regexp_v5_fmt.search(starterName):
                  #
                  # It's a v5 run
                  block_length=10
                  spmd_block='%10d'
                elif regexp_v4_fmt.search(starterName):
                  #
                  # It's a v4 run
                  block_length=8
                  spmd_block='%8d'

                #
                # Modify starter file to match required processors
                src=open(starterName,'r')
                dst=open(starterName + '_new','w')

                spmd=re.compile('^/SPMD')
                endofinput=re.compile('^/END')
                line=src.readline()
                spmdfound=0
                while line:
                  if spmd.match(line):
                    dst.write(line)
                    line=src.readline()
                    dst.write(line)
                    line=src.readline()
                    line_dst=line[:block_length] + spmd_block % int(os.environ['TOTALNCPUS']) + line[2 * block_length:]
                    dst.write(line_dst)
                    print "Found SPMD defininition in input file, substituting with:\n%s" % line_dst
                  elif endofinput.match(line):
                    print "Reached /END"
                    if ( spmdfound == 0 ):
                        line_dst=(spmd_block + spmd_block) % (0,int(os.environ['TOTALNCPUS']))
                        dst.write('/SPMD\r\n')
                        dst.write(line_dst + '\r\n')
                        dst.write('/END\r\n')
                        print "SPMD defininition not found in input file, inserting:\n/SPMD\n%s" % line_dst
                  else:
                    dst.write(line)
                  line=src.readline()

                src.close()
                dst.close()

                os.rename(starterName,starterName + '_original')
                os.rename(starterName + '_new',starterName)

                #setup starter command line
                cleanup_cmd = cleanup_cmd + " ./" + starterName
                starter_cmd = "%s/%s %s%s" % (
                os.environ['RADIR'], starterbin,"< ./",starterName )
                print starter_cmd
                os.system (starter_cmd)

sys.stdout.flush()

if ( os.environ['RUNTYPE'] == "engine" ) or ( os.environ['RUNTYPE'] == "both" ):
        engineNames=os.environ['ENGINEFILES'].split(';')
        if len(engineNames[0]) == 0:
                print "Engine run requested but engine file is not specified: skipping engine."
        else:
                #cycle on all the engine files
                i=0
                for i in range(0,len(engineNames)):
                        cleanup_cmd = cleanup_cmd + " ./" + os.path.basename(engineNames[i])
                i=0
                for i in range(0,len(engineNames)):

                        # Write current engine file name to disk
                        # for later usage from application aciotn scripts
                        f=open('currentEngineFile','w')
                        f.write(os.path.basename(engineNames[i]))
                        f.close()

                        if ( MPI_TYPE == "hpmpi" ):
                          # Build engine command line
                          engineName = os.path.basename(engineNames[i])
                          engine_cmd = os.environ['MPI_ROOT'] + "/bin/mpirun"
#                          engine_cmd = engine_cmd + " -cpu_bind=v,ll -stdio=i0 -e MPI_FLAGS=y,E"
                        # engine_cmd = engine_cmd + " -e ALTAIR_LICENSE_PATH=" + os.environ['ALTAIR_LICENSE_PATH']
                          engine_cmd = engine_cmd + " -e MPI_WORKDIR=" + os.environ['PBS_JOBDIR']
                          engine_cmd = engine_cmd + " -np " + os.environ['TOTALNCPUS']
                          engine_cmd = engine_cmd + " -hostfile " + os.environ['PBS_NODEFILE']
                          engine_cmd = engine_cmd + " " + enginebin
                          engine_cmd = engine_cmd + " < ./" + engineName
			else:
                          engine_cmd = "echo Sorry, this should not happen."

                        #run engine application
                        print engine_cmd
                        os.system (engine_cmd)
                        sys.stdout.flush()

# remove radflex*_linux and original input files or else they will be staged out
# this could lead to long wait times if the input data is large!!
#print cleanup_cmd
#os.system(cleanup_cmd)
sys.stdout.flush()
