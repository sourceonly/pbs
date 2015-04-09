#coding: utf-8

'''
© Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
This code is provided “as is” without any warranty, express or implied, or
indemnification of any kind. All other terms and conditions are as specified
in the Altair PBS Application Services EULA.
'''

import os
import sys
import shlex
import zipfile
import re
import subprocess
import shutil

__version__ = '12.1.0'


''' Importing Environment '''

if os.path.exists('%s/runtime/start.export' % os.environ['PBS_JOBDIR']):

    start_export = open('%s/runtime/start.export' % os.environ['PBS_JOBDIR'], 'r')

    for variable in start_export.readlines():

        if not variable.startswith('#'):

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

    start_export.close()

if os.path.exists('%s/runtime/actions.export' % os.environ['PBS_JOBDIR']):

    actions_export = open('%s/runtime/actions.export' % os.environ['PBS_JOBDIR'], 'r')

    for variable in actions_export.readlines():

        if not variable.startswith('#'):

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

    actions_export.close()

if os.path.exists('%s/runtime/exit.environment' % os.environ['PBS_JOBDIR']):

    exit_environment = open('%s/runtime/exit.environment' % os.environ['PBS_JOBDIR'], 'r')

    for variable in exit_environment.readlines():

        if re.match('(.*)=(.*)', variable):

            if not variable.startswith('#'):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    exit_environment.close()

if 'PAS_ENVIRONMENT' in os.environ:

    for variable in os.environ['PAS_ENVIRONMENT'].split(';'):

        if re.match('(.*)=(.*)', variable):

            if not variable.startswith('#'):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    del os.environ['PAS_ENVIRONMENT']


''' Logging '''

log = open('%s/exit.log' % os.environ['PBS_JOBDIR'], 'w')

logging = False

if 'PAS_LOGGING' in os.environ:

    if os.environ['PAS_LOGGING'] == 'true':
        logging = True
    elif os.environ['PAS_LOGGING'] == 'false':
        logging = False

''' Normalizing File Paths '''

if 'PAS_INPUT_FILE' in os.environ:
    os.environ['PAS_INPUT_FILE'] = os.path.basename(os.environ['PAS_INPUT_FILE'])

if 'PAS_MASTER_FILE' in os.environ:
    os.environ['PAS_MASTER_FILE'] = os.path.basename(os.environ['PAS_MASTER_FILE'])

if 'PAS_STARTER_FILE' in os.environ:
    os.environ['PAS_STARTER_FILE'] = os.path.basename(os.environ['PAS_STARTER_FILE'])

if 'PAS_ENGINE_FILE' in os.environ:
    os.environ['PAS_ENGINE_FILE'] = os.path.basename(os.environ['PAS_ENGINE_FILE'])

if 'PAS_RESTART_FILE' in os.environ:
    os.environ['PAS_RESTART_FILE'] = os.path.basename(os.environ['PAS_RESTART_FILE'])

if 'PAS_NASTRAN_FILE' in os.environ:
    os.environ['PAS_NASTRAN_FILE'] = os.path.basename(os.environ['PAS_NASTRAN_FILE'])

if 'PAS_PARAMETER_FILE' in os.environ:
    os.environ['PAS_PARAMETER_FILE'] = os.path.basename(os.environ['PAS_PARAMETER_FILE'])


''' Executing Exit Hook '''

if os.path.exists("%s/runtime/exit.hook" % os.environ['PBS_JOBDIR']):

    if logging is True:
        log.write('\nFound Exit Hook\n\n')

    command = "%s/runtime/exit.hook" % os.environ['PBS_JOBDIR']

    hook = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

    if logging is True:
        log.write('\n\tExit Hook Process ID: %s\n' % (hook.pid))

    for line in hook.stdout.readlines():

        if logging is True:
            log.write(line)

    hook.wait()

    if logging is True:
        log.write('\n\tExit Hook Return Code: %s\n' % (hook.returncode))

    if os.path.exists('%s/exit.import' % os.environ['PBS_JOBDIR']):

        exit_import = open('%s/exit.import' % os.environ['PBS_JOBDIR'], 'r')

        for variable in exit_import.readlines():

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

        exit_import.close()
else:

    if logging is True:
        log.write('\n\nNo Exit Hook Found\n')


''' Processing Environment '''

if logging is True:
    log.write('\nProcessing Environment\n')

for key, value in sorted(os.environ.items()):

    if re.search('PAS_', value):

        for k, v in sorted(os.environ.items(), reverse=True):

            if re.search('PAS_', k):

                pattern = re.compile(k, re.UNICODE)

                for match in pattern.findall(value):

                    value = re.sub(match, v, value)

                    try:
                        os.path.basename(value.strip())
                    finally:
                        os.environ[key.strip()] = value.strip()
if logging is True:

    for key, value in sorted(os.environ.items()):
        log.write('\n\t%s = %s' % (key.strip(), value.strip()))


''' Compress Results '''

if 'PAS_COMPRESS_RESULTS' in os.environ:
    if os.environ['PAS_COMPRESS_RESULTS'] == 'true':

        if logging is True:
            log.write('\n\nCompress Results Enabled\n')

        if 'PAS_COMPRESS_RESULTS_FORMAT' in os.environ:

            if logging is True:
                log.write('\n\tCompress Results Format: %s\n' % os.environ['PAS_COMPRESS_RESULTS_FORMAT'])

            if os.environ['PAS_COMPRESS_RESULTS_FORMAT'] == '.tar.gz':
                command = "tar --exclude='runtime/*' --exclude='pbs_spawn/*' -cvzf %s-results.tar.gz *" % os.environ['PAS_JOB_NAME']

            if os.environ['PAS_COMPRESS_RESULTS_FORMAT'] == '.zip':
                command = "zip -r %s-results.zip * -x runtime/** pbs_spawn/**" % os.environ['PAS_JOB_NAME']
        else:
            command = "zip -r %s-results.zip * -x runtime/** pbs_spawn/**" % os.environ['PAS_JOB_NAME']

        compress = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

        if logging is True:
            log.write('\n\tCompress Results Process ID: %s\n' % (compress.pid))

        for line in compress.stdout.readlines():

            if logging is True:
                log.write(line)

        compress.wait()

        ## This is somewhat how I'd like to remove all job files (minus the compressed results of course).

        #for root, dirs, files in os.walk(os.environ['PBS_JOBDIR'], topdown=False):
        #
        #    for name in files:
        #
        #        if not re.match('results', name):
        #            os.remove(os.path.join(root, name))
        #
        #    for name in dirs:
        #        os.rmdir(os.path.join(root, name))

''' Exporting Environment '''

exit_export = open('%s/runtime/exit.export' % os.environ['PBS_JOBDIR'], 'a')

for key, value in sorted(os.environ.items()):

    if re.search('PAS_', key):

        if not key.startswith('#'):

            exit_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

    elif re.search('PAS_', value):

        if not key.startswith('#'):

            exit_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

exit_export.close()

log.close()
sys.stdout.flush()
sys.exit(0)
