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

log = open('%s/start.log' % os.environ['PBS_JOBDIR'], 'w')

logging = False

if 'PAS_LOGGING' in os.environ:

    if os.environ['PAS_LOGGING'] == 'true':
        logging = True
    elif os.environ['PAS_LOGGING'] == 'false':
        logging = False


''' Normalize Paths '''


def normalize_path(variable):

    elements = os.environ[variable].split('/', 3)
    os.environ[variable] = os.path.basename(elements[3].strip())

    # I will find a more simplistic way of doing this.

    if 'PAS_CONVERT_TO_UNIX' in os.environ:
        if os.environ['PAS_CONVERT_TO_UNIX'] == 'true':

            file = os.environ[variable]

            if os.path.isdir(file):
                print file, "Directory!"

            data = open(file, "rb").read()

            if '\0' in data:
                print file, "Binary!"

            newdata = re.sub("\r\n", "\n", data)

            if newdata != data:

                print file
                f = open(file, "wb")
                f.write(newdata)
                f.close()

            if logging is True:
                log.write('\nConverting to UNIX Line Endings: %s\n' % os.environ[variable])

    #elif 'PAS_CONVERT_TO_WINDOWS' in os.environ:
    #    if os.environ['PAS_CONVERT_TO_WINDOWS'] == 'true':
    #
    #        file = os.environ[variable]
    #
    #        if os.path.isdir(file):
    #            print file, "Directory!"
    #
    #        data = open(file, "rb").read()
    #
    #        if '\0' in data:
    #            print file, "Binary!"
    #
    #        newdata = re.sub("\r?\n", "\r\n", data)
    #
    #        if newdata != data:
    #
    #            print file
    #            f = open(file, "wb")
    #            f.write(newdata)
    #            f.close()
    #
    #        if logging is True:
    #            log.write('\nConverting to Windows Line Endings: %s\n' % os.environ[variable])
    else:
        return True

if 'PAS_INPUT_FILE' in os.environ:
    normalize_path('PAS_INPUT_FILE')

if 'PAS_INPUT_FILE_ARRAY' in os.environ:

    input_file_array = os.environ['PAS_INPUT_FILE_ARRAY'].split(';')

    array = []

    for file in input_file_array:

        elements = os.environ['PAS_INPUT_FILE_ARRAY'].split('/', 3)
        array.append('/%s' % os.path.basename(elements[3].strip()))

    os.environ['PAS_INPUT_FILE_ARRAY'] = ';'.join(array)

if 'PAS_MASTER_FILE' in os.environ:
    normalize_path('PAS_MASTER_FILE')

if 'PAS_STARTER_FILE' in os.environ:
    normalize_path('PAS_STARTER_FILE')

if 'PAS_ENGINE_FILE' in os.environ:
    normalize_path('PAS_ENGINE_FILE')

if 'PAS_RESTART_FILE' in os.environ:
    normalize_path('PAS_RESTART_FILE')


''' Executing Start Hook '''

if os.path.exists("%s/runtime/start.hook" % os.environ['PBS_JOBDIR']):

    if logging is True:
        log.write('\nFound Start Hook\n\n')

    command = "%s/runtime/start.hook" % os.environ['PBS_JOBDIR']

    hook = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

    if logging is True:
        log.write('\n\tStart Hook Process ID: %s\n' % (hook.pid))

    for line in hook.stdout.readlines():

        if logging is True:
            log.write(line)

    hook.wait()

    if logging is True:
        log.write('\n\tStart Hook Return Code: %s\n' % (hook.returncode))

    ''' Import Environment from Start Hook '''

    if os.path.exists('%s/start.import' % os.environ['PBS_JOBDIR']):

        submit_export = open('%s/start.import' % os.environ['PBS_JOBDIR'], 'r')

        for variable in submit_export.readlines():

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

        submit_export.close()
else:

    if logging is True:
        log.write('\n\nNo Start Hook Found\n')

''' Script '''

if 'PAS_SCRIPT' in os.environ:

    if os.path.exists(os.environ['PAS_SCRIPT']):

        os.environ['PAS_SCRIPT_ACTUAL'] = os.environ['PAS_SCRIPT']
        os.environ['PAS_SCRIPT_BASENAME'] = os.path.basename(os.environ['PAS_SCRIPT'])
        os.environ['PAS_SCRIPT_ABSPATH'] = os.path.abspath(os.environ['PAS_SCRIPT'])

''' Input File Array '''

if 'PAS_INPUT_FILE_ARRAY' in os.environ:

    if logging is True:
        log.write('\n\nInput File Array Found\n')

    input_file_array = os.environ['PAS_INPUT_FILE_ARRAY'].split(';')

    if logging is True:
        log.write('\n\tInput File Array: %s\n' % input_file_array)

    if len(input_file_array) == 1:
        os.environ['PAS_INPUT_FILE'] = input_file_array[0]

        if logging is True:
            log.write('\n\tInput File: %s\n' % os.environ['PAS_INPUT_FILE'])

    elif len(input_file_array) >= 2:

        if 'PBS_ARRAY_INDEX' in os.environ:
            os.environ['PAS_INPUT_FILE'] = input_file_array[os.environ['PBS_ARRAY_INDEX']]

            if logging is True:
                log.write('\n\tJob Array Index: %s\n' % os.environ['PAS_INPUT_FILE'])

            if logging is True:
                log.write('\n\tInput File: %s\n' % os.environ['PAS_INPUT_FILE'])
        else:
            os.environ['PAS_INPUT_FILE'] = input_file_array[0]

            if logging is True:
                log.write('\n\tInput File: %s\n' % os.environ['PAS_INPUT_FILE'])


''' Normalize Archives '''

if 'PAS_NORMALIZE_ARCHIVES' in os.environ:
    if 'PAS_NORMALIZE_ARCHIVES' == 'true':

        if logging is True:
            log.write('\n\nNormalizing Archives\n')

        def process_file(file):

            if zipfile.is_zipfile(file):

                if logging is True:
                    log.write('\n\tFound ZIP Archive: %s\n' % (file))

                package = zipfile.ZipFile(file, 'r')

                for name in package.namelist():

                    if re.search('input', name, re.IGNORECASE):
                        os.environ['PAS_INPUT_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Input File: %s\n' % (name))

                    if re.search('master', name, re.IGNORECASE):
                        os.environ['PAS_MASTER_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Master File: %s\n' % (name))

                    if re.search('starter', name, re.IGNORECASE):
                        os.environ['PAS_STARTER_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Starter File: %s\n' % (name))

                    if re.search('engine', name, re.IGNORECASE):
                        os.environ['PAS_ENGINE_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Engine File: %s\n' % (name))

                    if re.search('restart', name, re.IGNORECASE):
                        os.environ['PAS_RESTART_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Restart File: %s\n' % (name))

                    if re.search('nastran', name, re.IGNORECASE):
                        os.environ['PAS_NASTRAN_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Nastran File: %s\n' % (name))

                    if re.search('parameter', name, re.IGNORECASE):
                        os.environ['PAS_PARAMETER_FILE'] = name

                        if logging is True:
                            log.write('\n\tFound Parameter File: %s\n' % (name))

                package.close

                os.system("unzip %s" % (file))
                sys.stdout.flush()

        if 'PAS_INPUT_FILE' in os.environ:
            process_file(os.environ['PAS_INPUT_FILE'])

        if 'PAS_MASTER_FILE' in os.environ:
            process_file(os.environ['PAS_MASTER_FILE'])

        if 'PAS_STARTER_FILE' in os.environ:
            process_file(os.environ['PAS_STARTER_FILE'])

        if 'PAS_ENGINE_FILE' in os.environ:
            process_file(os.environ['PAS_ENGINE_FILE'])

        if 'PAS_RESTART_FILE' in os.environ:
            process_file(os.environ['PAS_RESTART_FILE'])

        if 'PAS_NASTRAN_FILE' in os.environ:
            process_file(os.environ['PAS_NASTRAN_FILE'])

        if 'PAS_PARAMETER_FILE' in os.environ:
            process_file(os.environ['PAS_PARAMETER_FILE'])


''' The No Extension Functionality (useful for Abaqus) '''

if 'PAS_INPUT_FILE' in os.environ:
    os.environ['PAS_INPUT_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_INPUT_FILE'])[0])

if 'PAS_MASTER_FILE' in os.environ:
    os.environ['PAS_MASTER_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_MASTER_FILE'])[0])

if 'PAS_STARTER_FILE' in os.environ:
    os.environ['PAS_STARTER_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_STARTER_FILE'])[0])

if 'PAS_ENGINE_FILE' in os.environ:
    os.environ['PAS_ENGINE_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_ENGINE_FILE'])[0])

if 'PAS_RESTART_FILE' in os.environ:
    os.environ['PAS_RESTART_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_RESTART_FILE'])[0])

if 'PAS_NASTRAN_FILE' in os.environ:
    os.environ['PAS_NASTRAN_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_NASTRAN_FILE'])[0])

if 'PAS_PARAMETER_FILE' in os.environ:
    os.environ['PAS_PARAMETER_FILE_NO_EXT'] = os.path.basename(os.path.splitext(os.environ['PAS_PARAMETER_FILE'])[0])


''' Transfer Include Files '''

if 'PAS_TRANSFER_INCLUDE_FILES' in os.environ:
    if os.environ['PAS_TRANSFER_INCLUDE_FILES'] == 'true':

        if logging is True:
            log.write('\n\nTransfer Include Files\n')

        command = "%s/runtime/include_parser.py" % os.environ['PBS_JOBDIR']

        shell = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

        for line in shell.stdout.readlines():

            if logging is True:
                log.write(line)

        shell.wait()


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


''' Run Executable '''

if 'PAS_EXECUTABLE' in os.environ:
    if os.path.exists(os.environ['PAS_EXECUTABLE']):
        if os.access(os.environ['PAS_EXECUTABLE'], os.X_OK):

            if logging is True:
                log.write('\n\nFound Executable: %s\n\n' % (os.environ['PAS_EXECUTABLE']))

            if 'PAS_ARGUMENTS' in os.environ:
                command = '%s %s' % (os.environ['PAS_EXECUTABLE'], os.environ['PAS_ARGUMENTS'])
            else:
                command = os.environ['PAS_EXECUTABLE']

            if 'PAS_RUN_PARALLEL' in os.environ:
                if os.environ['PAS_RUN_PARALLEL'] == 'true':

                    if logging is True:
                        log.write('\n\tRun Parallel Enabled\n')

                    command = ("%s/runtime/qlaunch.sh %s" % (os.environp['PBS_JOBDIR'], command))

            if logging is True:
                log.write('\n\tCommand: %s\n' % (command))

            executable = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

            if logging is True:
                log.write('\n\tExecutable Process ID: %s\n' % (executable.pid))

            start_executable_pid = open('%s/runtime/start.executable.pid' % os.environ['PBS_JOBDIR'], 'w')
            start_executable_pid.write('%s\n' % (executable.pid))
            start_executable_pid.close()

            for line in executable.stdout.readlines():

                if logging is True:
                    log.write(line)

            executable.wait()

            if logging is True:
                log.write('\n\tExecutable Return Code: %s\n' % (executable.returncode))
        else:

            if logging is True:

                log.write('\nFound Executable: %s\n\n' % (os.path.basename(os.environ['PAS_EXECUTABLE'])))
                log.write('\nYour Executable does not appear to be executable.\n\n')
else:

    if logging is True:
        log.write('\n\nNo Executable Found\n')


''' Run Script '''


def get_interpreter(shell_script):

    file = open(shell_script, 'r')
    line = file.readline()
    file.close()

    if line.startswith('#!'):
        try:
            interpreter = re.match('^#!(.*)', line).group(1)
            return interpreter
        except OSError:
            print >> sys.stderr, ('\n\tAn error occurred while opening PAS_SCRIPT.')
    else:
        try:
            print >> sys.stdout, ('\n\tNo #! (shebang) line detected in PAS_SCRIPT. Defaulting to Python.')
            return os.environ['PAS_PYTHON_PATH']
        except OSError:
            print >> sys.stderr, ('\n\tAn error occurred while detecting the #! line of PAS_SCRIPT.')

if 'PAS_SCRIPT' in os.environ:
    if os.path.exists(os.path.basename(os.environ['PAS_SCRIPT'])):
        if os.access(os.path.basename(os.environ['PAS_SCRIPT']), os.X_OK):

            if logging is True:
                log.write('\n\nFound Script: %s\n\n' % (os.path.basename(os.environ['PAS_SCRIPT'])))

            shell_script = os.path.abspath(os.path.basename(os.environ['PAS_SCRIPT']))
            interpreter = get_interpreter(shell_script)

            if 'PAS_ARGUMENTS' in os.environ:
                command = '%s %s %s' % (interpreter, shell_script, os.environ['PAS_ARGUMENTS'])
            else:
                command = '%s %s' % (interpreter, shell_script)

            if 'PAS_RUN_PARALLEL' in os.environ:
                if os.environ['PAS_RUN_PARALLEL'] == 'true':

                    if logging is True:
                        log.write('\n\tRun Parallel Enabled\n')

                    ### This seems to be working fine but I'll keep an eye on it.
                    command = ("%s/runtime/qlaunch.sh %s" % (os.environ['PBS_JOBDIR'], command))

            if logging is True:
                log.write('\n\tCommand: %s\n' % (command))

            script = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

            if logging is True:
                log.write('\n\tScript Process ID: %s\n' % (script.pid))

            start_script_pid = open('%s/runtime/start.script.pid' % os.environ['PBS_JOBDIR'], 'w')
            start_script_pid.write('%s\n' % (script.pid))
            start_script_pid.close()

            for line in script.stdout.readlines():

                if logging is True:
                    log.write(line)

            script.wait()

            if logging is True:
                log.write('\n\tScript Return Code: %s\n' % (script.returncode))
        else:

            if logging is True:

                log.write('\nFound Script: %s\n\n' % (os.path.basename(os.environ['PAS_SCRIPT'])))
                log.write('\n\tYour Script does not appear to be executable.\n')
else:

    if logging is True:
        log.write('\n\nNo Script Found\n')


''' Exporting Environment '''

start_export = open('%s/runtime/start.export' % os.environ['PBS_JOBDIR'], 'a')

for key, value in sorted(os.environ.items()):

    if re.search('PAS_', key):

        if not key.startswith('#'):

            start_export.write('%s=%s\n' % (key, value))

            if not key == 'PAS_PYTHON_PATH':
                del os.environ[key]

    elif re.search('PAS_', value):

        if not key.startswith('#'):

            start_export.write('%s=%s\n' % (key, value))

            if not key == 'PAS_PYTHON_PATH':
                del os.environ[key]

start_export.close()


log.close()
sys.stdout.flush()


''' Exit Phase '''

if os.path.exists("%s/runtime/exit.py" % os.environ['PBS_JOBDIR']):

    command = ("%s %s/runtime/exit.py" % (os.environ['PAS_PYTHON_PATH'], os.environ['PBS_JOBDIR']))

    exit_phase = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)
    exit_phase.wait()

sys.stdout.flush()
sys.exit(0)
