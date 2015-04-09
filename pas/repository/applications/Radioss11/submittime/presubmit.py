#!/usr/bin/python
# purpose: update job attributes if required
#
# the following objects are available during script execution:
# "job": PBS job which is ready for submission
# "userInputs": dictionary with all inputs from user
# "policies": dictionary with all policies as defined in AIF
# 

import time
import os
import sys

DEBUG=0

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

if DEBUG:
  f=open('/tmp/presubmit.debug','w')
  print "Executing presubmit.py script...\n"
  job.attr_destination=userInputs['QUEUE']

#'''
#  Print environment
#'''
  f.write('userInputs:\n')
  for k in sorted(list(userInputs)):
    f.write(k)
    f.write(' = ')
    f.write(userInputs[k])
    f.write('\n')
  f.write('\n')

  f.write('policies:\n')
  for k in sorted(list(policies)):
    f.write(k)
    f.write(' = ')
    f.write(policies[k])
    f.write('\n')
  f.write('\n')

  f.write('environment:\n')
  for k in sorted(list(os.environ)):
    f.write(k)
    f.write(' = ')
    f.write(os.environ[k])
    f.write('\n')
  f.write('\n')


  f.write('Job resource request: ')
  f.write(str(job.attr_resource))
  f.write('\n')

#'''
#  Create a dictionary out of job.attr_resources
#'''
resources = {}
for res in job.attr_resource.split(';'):
  resources[res.split('=',1)[0]]=res.split('=',1)[1]

#'''
#  Compute correct number of hyperworks tokens to be used
#'''
hosts=int(userInputs['HOSTS'])
cores=int(userInputs['CORES'])
#ncpus=str(hosts * cores)
if ( userInputs['RUNTYPE'].lower() == 'starter' ):
  resources['hyperworks']='1000'
else:
  ncpus=(hosts * cores)
#  ncpus=str(hosts * cores)
  if ncpus <=4:
    resources['hyperworks']='25000'
  elif ( 4 < ncpus ) and ( ncpus <= 8 ):
    resources['hyperworks']='30000'
  elif ( 8 < ncpus ) and ( ncpus <= 12 ):
    resources['hyperworks']='34000'
  elif ( 12 < ncpus ) and ( ncpus <= 16 ):
    resources['hyperworks']='38000'
  elif ( 16 < ncpus ) and ( ncpus <= 24 ):
    resources['hyperworks']='44000'
  elif ( 24 < ncpus ) and ( ncpus <= 32 ):
    resources['hyperworks']='50000'
  elif ( 32 < ncpus ) and ( ncpus <= 48 ):
    resources['hyperworks']='75000'
  elif ( 48 < ncpus ) and ( ncpus <= 64 ):
    resources['hyperworks']='75000'
  elif ( 64 < ncpus ):
    resources['hyperworks']='75000'
  
#'''
#  Rebuild job.attr_resources
#'''
job.attr_resource = ''
for res in resources.keys():
  job.attr_resource += res + '=' + resources[res] + ';'






if DEBUG:
  f.write('Cooked ')
  f.write('job resource request: ')
  f.write(str(job.attr_resource))
  f.write('\n')

  print "Execution of presubmit.py script terminated.\n"
  f.close()

sys.stdout.flush()
