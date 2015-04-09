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

print "Executing presubmit.py script of application interactiveApp\n"

# job attributes which can be modified if required:
#job.attr_job_owner="ghavin"
#job.attr_date_time
#job.attr_accounting_label = policies['STD_ACCOUNT']
#job.attr_interval
#job.attr_directive_prefix
#job.attr_error_path="tr-cave02.prog.altair.com:/tmp/ehwodTest999"
#job.attr_user_hold_job
#job.attr_join
#job.attr_job_array
#job.attr_keep_streams
#job.attr_resource="software=optistruct,GWU=71,select=1:mem=30mb:ncpus=2:aif_applications_enabled=optistruct"
#job.attr_mail_options=userInputs['MAIL_POINTS'] 
#job.attr_mail_options
#job.attr_mail_list=userInputs['MAIL_USERS']
#job.attr_job_name = userInputs['JOB_NAME'] + "_modified"
#job.attr_output_path="tr-cave02.prog.altair.com:/tmp/ohwodTest999"
#job.attr_job_priority
job.attr_destination = "iworkq"
#job.attr_destination = userInputs['QUEUE_NAME']
#job.attr_job_rerunable
#job.attr_shell_path_list
#job.attr_user_list
#job.attr_additional_attrs
#job.attr_export_env_to_job
#job.attr_export_all_user_env
#job.attr_no_jobid_stdout
#job.attr_script
#job.attr_status
#job.attr_stagein_list= "pbs_spawn@tr-pc69:/opt/gridworks/11.0.0/aif/pbs_spawn"
#job.attr_stagein_list= "n/a"
#job.attr_stageout_list = "n/a"
#job.attr_sandbox = "n/a"
#job.attr_job_owner

sys.stdout.flush()

