#!/usr/bin/python
#
# (c) Copyright 2010 Altair Engineering, Inc.  All rights reserved.
#
# This code is provided as is without any warranty, express or implied,
# or indemnification of any kind.
# All other terms and conditions are as specified in the Altair PBS EULA.
#

# purpose: update job attributes if required
#
# the following objects are available during script execution:
# "job": PBS job which is ready for submission
# "userInputs": dictionary with all inputs from user
# "policies": dictionary with all policies as defined in AIF
# 
# job attributes which can be modified if required:
#job.attr_job_owner="ghavin"
#job.attr_date_time
#job.attr_accounting_label = policies['STD_ACCOUNT']
#job.attr_interval
#job.attr_directive_prefix
#job.attr_error_path
#job.attr_user_hold_job
#job.attr_join
#job.attr_job_array
#job.attr_keep_streams
#job.attr_resource="software=optistruct,GWU=71,select=1:mem=30mb:ncpus=2:aif_applications_enabled=optistruct"
#job.attr_mail_options
#job.attr_mail_list
#job.attr_job_name = userInputs['JOB_NAME'] + "_modified"
#job.attr_output_path
#job.attr_job_priority
#job.attr_destination
#job.attr_job_rerunable
#job.attr_shell_path_list
#job.attr_user_list
#job.attr_additional_attrs
#job.attr_export_env_to_job
#job.attr_export_all_user_env
#job.attr_no_jobid_stdout
#job.attr_script
#job.attr_status
#job.attr_stagein_list
#job.attr_stageout_list
#job.attr_sandbox
#job.attr_job_owner

import os
import sys

#'''
#   To enable presubmit debug mode, create a site policy named
#   PRESUBMIT_DEBUG and make its value greater than 0.
#   1 - Yes
#   0 - No
#'''
DEBUG=0
PRESUBMIT_DEBUG_FILE='presubmit.debug'
if ( 'PRESUBMIT_DEBUG' in policies ) and ( 'PRESUBMIT_DEBUG_FILE' in policies ):
  DEBUG=int(policies['PRESUBMIT_DEBUG'])
  DEBUG_FILE=policies['PRESUBMIT_DEBUG_FILE']

#'''
#   If debug mode is on, every now and then this script will
#   will write debugging informations in DEBUG_FILE
#'''
if DEBUG:
  f=open(DEBUG_FILE,'w')
  print "Executing presubmit.py script...\n"

  #'''
  #  Print user inputs to DEBUG_FILE
  #'''
  f.write('userInputs:\n')
  for k in sorted(list(userInputs)):
    f.write(k)
    f.write(' = ')
    f.write(userInputs[k])
    f.write('\n')
  f.write('\n')

  #'''
  #   Print policies to DEBUG_FILE
  #'''
  f.write('policies:\n')
  for k in sorted(list(policies)):
    f.write(k)
    f.write(' = ')
    f.write(policies[k])
    f.write('\n')
  f.write('\n')

  #'''
  #   Print environment  contents to DEBUG_FILE
  #'''
  f.write('environment:\n')
  for k in sorted(list(os.environ)):
    f.write(k)
    f.write(' = ')
    f.write(os.environ[k])
    f.write('\n')
  f.write('\n')

  #'''
  #   Print resource requests as they came from app-conv translation to DEBUG_FILE
  #'''
  f.write('Job resource request: ')
  f.write(str(job.attr_resource))
  f.write('\n')

#'''
#   Set job destination QUEUE according to user input
#'''
job.attr_destination=userInputs['QUEUE']

#'''
#   Create a dictionary out of job.attr_resources
#'''
resources = {}
for res in job.attr_resource.split(';'):
  resources[res.split('=',1)[0]]=res.split('=',1)[1]

#'''
#   Compute correct number of GridWorks tokens to be used.
#   For this to work, you must configure site policy ALTAIR_GRIDWORKS_RESOURCE
#   to contain the PBS resource name to request for GridWorks tokens
#'''
#if ( 'ALTAIR_GRIDWORKS_RESOURCE' in policies ):
#  ALTAIR_GRIDWORKS_RESOURCE=policies['ALTAIR_GRIDWORKS_RESOURCE']
#  ncpus=int(userInputs['CORES'])
#  if ncpus <=4:
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='2500'
#  elif ( 4 < ncpus ) and ( ncpus <= 8 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='3000'
#  elif ( 8 < ncpus ) and ( ncpus <= 12 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='3400'
#  elif ( 12 < ncpus ) and ( ncpus <= 16 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='3800'
#  elif ( 16 < ncpus ) and ( ncpus <= 24 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='4400'
#  elif ( 24 < ncpus ) and ( ncpus <= 32 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='5000'
#  elif ( 32 < ncpus ) and ( ncpus <= 48 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='7500'
#  elif ( 48 < ncpus ) and ( ncpus <= 64 ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='7500'
#  elif ( 64 < ncpus ):
#    resources[ALTAIR_GRIDWORKS_RESOURCE]='7500'
  
#'''
#   Rebuild job.attr_resources from the tweaked list
#'''
job.attr_resource = ''
for res in resources.keys():
  job.attr_resource += res + '=' + resources[res] + ';'

#'''
#   Print processed job resource requests and parameters
#'''
if DEBUG:
  f.write('Cooked ')
  f.write('job resource request: ')
  f.write(str(job.attr_resource))
  f.write('\n')

  print "Execution of presubmit.py script terminated.\n"
  f.close()

sys.stdout.flush()
