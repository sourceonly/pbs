#coding: utf-8

'''
© Copyright 2013 Altair Engineering, Inc. All rights reserved.
This code is provided “as is” without any warranty, express or implied, or
indemnification of any kind. All other terms and conditions are as specified
in the Altair PBS Application Services EULA.
'''

import os
import sys
import re
import signal
import subprocess

__version__ = '12.1.0'


''' Importing Environment '''

if os.path.exists('%s/runtime/submit.export.%s' % (os.environ['PBS_JOBDIR'], os.environ['PAS_JOB_NAME'])):

    submit_export = open('%s/runtime/submit.export.%s' % (os.environ['PBS_JOBDIR'], os.environ['PAS_JOB_NAME']), 'r')

    for variable in submit_export.readlines():

        if not variable.startswith('#'):

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

    submit_export.close()

if os.path.exists('%s/runtime/start.environment' % os.environ['PBS_JOBDIR']):

    start_environment = open('%s/runtime/start.environment' % os.environ['PBS_JOBDIR'], 'r')

    for variable in start_environment.readlines():

        if re.match('(.*)=(.*)', variable):

            if not variable.startswith('#'):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    start_environment.close()

if 'PAS_ENVIRONMENT' in os.environ:

    for variable in os.environ['PAS_ENVIRONMENT'].split(';'):

        if re.match('(.*)=(.*)', variable):

            if not variable.startswith('#'):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    del os.environ['PAS_ENVIRONMENT']


''' Logging '''

log = open('%s/actions.log' % os.environ['PBS_JOBDIR'], 'w')

logging = False

if 'PAS_LOGGING' in os.environ:

    if os.environ['PAS_LOGGING'] == 'true':
        logging = True
    elif os.environ['PAS_LOGGING'] == 'false':
        logging = False


''' Exporting Actions Environment '''

if os.path.exists('%s/runtime/actions.environment' % os.environ['PBS_JOBDIR']):

    path = '%s/runtime/actions.environment' % os.environ['PBS_JOBDIR']

    if logging is True:
        log.write('\n\nFound Actions Environment File: %s\n' % (path))

    actions_environment = open(path, 'r')

    for variable in actions_environment.readlines():

        if re.match('(.*)=(.*)', variable):

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

    actions_environment.close()

else:

    if logging is True:
        log.write('\n\nNo Actions Environment File Found\n')


''' Executing Actions Hook '''

if os.path.exists("%s/runtime/actions.hook" % os.environ['PBS_JOBDIR']):

    if logging is True:
        log.write('\nFound Actions Hook\n\n')

    command = "%s/runtime/actions.hook" % os.environ['PBS_JOBDIR']

    hook = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

    if logging is True:
        log.write('\n\tActions Hook Process ID: %s\n' % (hook.pid))

    for line in hook.stdout.readlines():

        if logging is True:
            log.write(line)

    hook.wait()

    if logging is True:
        log.write('\n\tActions Hook Return Code: %s\n' % (hook.returncode))

    if os.path.exists('%s/actions.import' % os.environ['PBS_JOBDIR']):

        environment_import = open('%s/actions.import' % os.environ['PBS_JOBDIR'], 'r')

        for variable in environment_import.readlines():

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

        environment_import.close()
else:

    if logging is True:
        log.write('\n\nNo Actions Hook Found\n')


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
                    os.environ[key.strip()] = value.strip()

if logging is True:

    for key, value in sorted(os.environ.items()):
        log.write('\n\t%s = %s' % (key.strip(), value.strip()))


''' Send Signals '''

if 'PAS_ACTION_SEND_SIGNALS' in os.environ:

    if logging is True:
        log.write('\n\nSend Signals\n')

    def send_signal(process_file):

        pid_file = open(process_file, 'r')
        pid_num = int(pid_file.readline())
        pid_file.close()

        signal_name = os.environ['PAS_ACTION_SEND_SIGNALS']

        if signal_name == 'Suspend':

            os.kill(pid_num, signal.SIGTSTP)
            sys.stdout.write('Suspend signal sent.')

        elif signal_name == 'Resume':

            os.kill(pid_num, signal.SIGCONT)
            sys.stdout.write('Resume signal sent.')

        elif signal_name == 'Terminate':

            os.kill(pid_num, signal.SIGTERM)
            sys.stdout.write('Terminate signal sent.')

    if os.path.exists('%s/runtime/start.executable.pid' % os.environ['PBS_JOBDIR']):
        send_signal('%s/runtime/start.executable.pid' % os.environ['PBS_JOBDIR'])

        if logging is True:
            log.write('\n\tSending Signal to Executable: %s\n' % (os.environ['PAS_ACTION_SEND_SIGNALS']))

    if os.path.exists('%s/runtime/start.script.pid' % os.environ['PBS_JOBDIR']):
        send_signal('%s/runtime/start.script.pid' % os.environ['PBS_JOBDIR'])

        if logging is True:
            log.write('\n\tSending Signal to Script: %s\n' % (os.environ['PAS_ACTION_SEND_SIGNALS']))

'''Shell Command'''

if 'PAS_ACTION_SHELL_COMMAND' in os.environ:

    if logging is True:
        log.write('\n\nShell Command\n')

    os.system(os.environ['PAS_ACTION_SHELL_COMMAND'].strip())

    if logging is True:
        log.write('\n\tExecuting Shell Command: %s\n' % (os.environ['PAS_ACTION_SHELL_COMMAND']))


''' Exporting Environment '''

actions_export = open('%s/runtime/actions.export' % os.environ['PBS_JOBDIR'], 'a')

for key, value in sorted(os.environ.items()):

    if re.search('PAS_', key):

        if not key.startswith('#'):

            actions_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

    elif re.search('PAS_', value):

        if not key.startswith('#'):

            actions_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

actions_export.close()


log.close()
sys.stdout.flush()
sys.exit(0)
