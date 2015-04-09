#coding: utf-8

'''
© Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
This code is provided “as is” without any warranty, express or implied, or
indemnification of any kind. All other terms and conditions are as specified
in the Altair PBS Application Services EULA.
'''

import time
import re
import grp
import pwd
import os
import sys
import shutil
import subprocess

__version__ = '12.1.0'


''' Importing Environment '''

for variable in job.attr_export_env_to_job.split(','):

    (key, value) = variable.split('=', 1)
    os.environ[key.strip()] = value.strip()

if 'PAS_SUBMISSION_DIRECTORY' in os.environ:

    elements = os.environ['PAS_SUBMISSION_DIRECTORY'].split('/', 3)
    os.environ['PAS_USER_STAGE'] = '/%s' % (elements[3].strip())
    os.chdir(os.environ['PAS_USER_STAGE'])

if os.path.exists('/etc/pas.conf'):

    conf = open('/etc/pas.conf', 'r')

    for line in conf.readlines():

        if re.match('PAS_HOME', line):

            (key, value) = line.split('=')

            app_home = ('%s/repository/applications/%s'
                        % (value.strip(), os.environ['PAS_APPLICATION']))

            os.environ['PAS_APP_HOME'] = app_home.strip()

    conf.close()

elif 'PAS_CONF_FILE' in os.environ:

    if os.path.exists(os.environ['PAS_CONF_FILE']):

        conf = open(os.environ['PAS_CONF_FILE'], 'r')

        for line in conf.readlines():

            if re.match('PAS_HOME', line):

                (key, value) = line.split('=')

                app_home = ('%s/repository/applications/%s'
                            % (value.strip(), os.environ['PAS_APPLICATION']))

                os.environ['PAS_APP_HOME'] = app_home.strip()

        conf.close()
else:

    sys.stderr.write('\n\nThe pas.conf file could not be found.\n')
    sys.exit(1)

if os.path.exists('%s/submittime/submit.environment' % (os.environ['PAS_APP_HOME'])):

    path = ('%s/submittime/submit.environment' % (os.environ['PAS_APP_HOME']))

    submit_environment = open(path, 'r')

    for variable in submit_environment.readlines():

        if not variable.startswith('#'):

            if re.match('(.*)=(.*)', variable):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    submit_environment.close()

if 'PAS_ENVIRONMENT' in os.environ:

    for variable in os.environ['PAS_ENVIRONMENT'].split(';'):

        if re.match('(.*)=(.*)', variable):

            if not variable.startswith('#'):

                (key, value) = variable.split('=', 1)
                os.environ[key.strip()] = value.strip()

    del os.environ['PAS_ENVIRONMENT']


''' Logging '''

log = open('submit.log', 'w', 0644)
logging = False

if 'PAS_LOGGING' in os.environ:

    if os.environ['PAS_LOGGING'] == 'true':
        logging = True

    elif os.environ['PAS_LOGGING'] == 'false':
        logging = False


''' Normalize Paths '''


def normalize_path(variable):

    try:
        os.environ['%s_ACTUAL' % (variable)] = os.environ[variable]
        elements = os.environ[variable].split('/', 3)
        os.environ[variable] = '/%s' % (elements[3].strip())

    except:
        sys.stderr.write('\n\nSome strange error occurred normalizing: %s\n' % (os.environ[variable]))

if 'PAS_INPUT_FILE' in os.environ:
    normalize_path('PAS_INPUT_FILE')
    os.environ['PAS_INPUT_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_INPUT_FILE']))[0]

if 'PAS_INPUT_FILE_ARRAY' in os.environ:

    input_file_array = os.environ['PAS_INPUT_FILE_ARRAY'].split(';')

    array = []

    for file in input_file_array:
        array.append(os.path.abspath(elements[3].strip()))

    os.environ['PAS_INPUT_FILE_ARRAY'] = ';'.join(array)

if 'PAS_MASTER_FILE' in os.environ:
    normalize_path('PAS_MASTER_FILE')
    os.environ['PAS_MASTER_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_MASTER_FILE']))[0]

if 'PAS_STARTER_FILE' in os.environ:
    normalize_path('PAS_STARTER_FILE')
    os.environ['PAS_STARTER_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_STARTER_FILE']))[0]

if 'PAS_ENGINE_FILE' in os.environ:
    normalize_path('PAS_ENGINE_FILE')
    os.environ['PAS_ENGINE_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_ENGINE_FILE']))[0]

if 'PAS_RESTART_FILE' in os.environ:
    normalize_path('PAS_RESTART_FILE')
    os.environ['PAS_RESTART_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_RESTART_FILE']))[0]

if 'PAS_NASTRAN_FILE' in os.environ:
    normalize_path('PAS_NASTRAN_FILE')
    os.environ['PAS_NASTRAN_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_NASTRAN_FILE']))[0]

if 'PAS_PARAMETER_FILE' in os.environ:
    normalize_path('PAS_PARAMETER_FILE')
    os.environ['PAS_PARAMETER_FILE_NO_EXT'] = os.path.splitext(os.path.basename(os.environ['PAS_PARAMETER_FILE']))[0]


''' Executing Submit Hook '''

if os.path.exists("%s/submittime/submit.hook" % (os.environ['PAS_APP_HOME'])):

    if logging is True:
        log.write('\nFound Submit Hook\n\n')

    command = "%s/submittime/submit.hook" % (os.environ['PAS_APP_HOME'])

    hook = subprocess.Popen(command, env=os.environ, shell=True, stdout=subprocess.PIPE)

    if logging is True:
        log.write('\n\tSubmit Hook Process ID: %s\n' % (hook.pid))

    for line in hook.stdout.readlines():

        if logging is True:
            log.write(line)

    hook.wait()

    if logging is True:
        log.write('\n\tSubmit Hook Return Code: %s\n' % (hook.returncode))

    if os.path.exists('submit.import'):

        submit_import = open('submit.import', 'r')

        for variable in submit_import.readlines():

            (key, value) = variable.split('=', 1)
            os.environ[key.strip()] = value.strip()

        submit_import.close()
else:

    if logging is True:
        log.write('\n\nNo Submit Hook Found\n')


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


''' Processing Resources '''

if logging is True:
    log.write('\n\nProcessing Resources\n')

resources = ''

if 'PAS_SOFTWARE' in os.environ:

    resources = ('software=%s ' % (os.environ['PAS_SOFTWARE'].strip()))

    if logging is True:

        log.write('\n\tSoftware = %s'
                  % (os.environ['PAS_SOFTWARE'].strip()))

elif 'PAS_APPLICATION' in os.environ:

    resources = ('software=%s ' % (os.environ['PAS_APPLICATION'].strip()))

    if logging is True:
        log.write('\n\tApplication = %s'
                  % (os.environ['PAS_APPLICATION'].strip()))

if 'PAS_WALLTIME' in os.environ:

    resources = ('%s walltime=%s' % (resources, os.environ['PAS_WALLTIME'].strip()))

    if logging is True:
        log.write('\n\tWalltime = %s'
                  % (os.environ['PAS_WALLTIME'].strip()))

if 'PAS_PLACE' in os.environ:

    resources = ('%s place=%s' % (resources, os.environ['PAS_PLACE']))

    if logging is True:
        log.write('\n\tPlace = %s'
                  % (os.environ['PAS_PLACE'].strip()))

if 'PAS_SELECT' in os.environ:

    if 'PAS_SELECT_PREPEND' in os.environ:

        resources = ('%s %s+select=%s' % (resources, os.environ['PAS_SELECT_PREPEND'].strip(),
                                          os.environ['PAS_SELECT'].strip()))
        if logging is True:
            log.write('\n\tSelect Prepend = %s'
                      % (os.environ['PAS_SELECT_PREPEND'].strip()))
    else:

        resources = ('%s select=%s' % (resources, os.environ['PAS_SELECT'].strip()))

    if logging is True:
        log.write('\n\tSelect = %s'
                  % (os.environ['PAS_SELECT'].strip()))
else:
    resources = '%s select=1' % resources

if 'PAS_NCPUS' in os.environ:

    resources = ('%s:ncpus=%s' % (resources, os.environ['PAS_NCPUS'].strip()))

    if logging is True:
        log.write('\n\tNcpus = %s' % (os.environ['PAS_NCPUS'].strip()))

if 'PAS_NGPUS' in os.environ:

    resources = ('%s:ngpus=%s' % (resources, os.environ['PAS_NGPUS'].strip()))

    if logging is True:
        log.write('\n\tNgpus = %s' % (os.environ['PAS_NGPUS'].strip()))

if 'PAS_MPIPROCS' in os.environ:

    resources = ('%s:mpiprocs=%s' % (resources, os.environ['PAS_MPIPROCS'].strip()))

    if logging is True:
        log.write('\n\tMpiprocs = %s' % (os.environ['PAS_MPIPROCS'].strip()))

if 'PAS_OMPTHREADS' in os.environ:

    resources = ('%s:ompthreads=%s' % (resources, os.environ['PAS_OMPTHREADS'].strip()))

    if logging is True:
        log.write('\n\tOmpthreads = %s' % (os.environ['PAS_OMPTHREADS'].strip()))

if 'PAS_MEM' in os.environ:

    resources = ('%s:mem=%s' % (resources, os.environ['PAS_MEM'].strip()))

    if logging is True:
        log.write('\n\tMem = %s'
                  % (os.environ['PAS_MEM'].strip()))

if 'PAS_VMEM' in os.environ:

    resources = ('%s:vmem=%s' % (resources, os.environ['PAS_VMEM'].strip()))

    if logging is True:
        log.write('\n\tVmem = %s'
                  % (os.environ['PAS_VMEM'].strip()))

if 'PAS_ARCH' in os.environ:

    resources = ('%s:arch=%s' % (resources, os.environ['PAS_ARCH'].strip()))

    if logging is True:
        log.write('\n\tArch = %s'
                  % (os.environ['PAS_ARCH'].strip()))

if 'PAS_VNODE' in os.environ:

    resources = ('%s:vnode=%s' % (resources, os.environ['PAS_VNODE'].strip()))

    if logging is True:
        log.write('\n\tVnode = %s'
                  % (os.environ['PAS_VNODE'].strip()))

if 'PAS_SELECT_APPEND' in os.environ:

    resources = ('%s:%s' % (resources, os.environ['PAS_SELECT_APPEND'].strip()))

    if logging is True:
        log.write('\n\tSelect Append = %s'
                  % (os.environ['PAS_SELECT_APPEND'].strip()))

if 'PAS_RESOURCES' in os.environ:

    resources = os.environ['PAS_RESOURCES']

    if logging is True:
        log.write('\n\tResources = %s'
                  % (os.environ['PAS_RESOURCES'].strip()))

if logging is True:
    log.write('\n\tResource Statement to PBS = %s'
              % (resources.strip()))

job.attr_resource = resources.strip()


''' Processing Attributes '''

if logging is True:
    log.write('\n\nProcessing Attributes\n')

attributes = []

if 'PAS_ATTRIBUTES' in os.environ:

    if re.search('\w+', os.environ['PAS_ATTRIBUTES']):

        for attribute in os.environ['PAS_ATTRIBUTES'].split(','):
            attributes.append(attribute)

        if logging is True:
            log.write('\n\tAttributes = %s'
                      % (os.environ['PAS_ATTRIBUTES'].strip()))

if 'PAS_DEPEND' in os.environ:

    if re.search('\w+', os.environ['PAS_DEPEND']):

        attributes.append('depend=%s'
                          % (os.environ['PAS_DEPEND'].strip()))

        if logging is True:
            log.write('\n\tDependancy = %s'
                      % (os.environ['PAS_DEPEND'].strip()))

if 'PAS_GROUP_LIST' in os.environ:

    if re.search('\w+', os.environ['PAS_GROUP_LIST']):

        attributes.append('group_list=%s'
                          % (os.environ['PAS_GROUP_LIST'].strip()))

        if logging is True:
            log.write('\n\tGroup List = %s'
                      % (os.environ['PAS_GROUP_LIST'].strip()))

if 'PAS_ACCOUNT' in os.environ:

    if re.search('\w+', os.environ['PAS_ACCOUNT']):

        job.attr_accounting_label = os.environ['PAS_ACCOUNT'].strip()

        if logging is True:
            log.write('\n\tAccount = %s'
                      % (os.environ['PAS_ACCOUNT']).strip())

if 'PAS_PROJECT' in os.environ:

    job.attr_project = os.environ['PAS_PROJECT']

    if logging is True:
        log.write('\n\tProject = %s'
                  % (os.environ['PAS_PROJECT']))

if 'PAS_QUEUE' in os.environ:

    job.attr_destination = os.environ['PAS_QUEUE']

    if logging is True:
        log.write('\n\tQueue = %s'
                  % (os.environ['PAS_QUEUE']))

if 'PAS_MAIL_POINTS' in os.environ:

    if re.match(r"[abe]", os.environ['PAS_MAIL_POINTS']):
        job.attr_mail_options = os.environ['PAS_MAIL_POINTS'].strip()

    if logging is True:
        log.write('\n\tMail Points = %s'
                  % (os.environ['PAS_MAIL_POINTS']))

if 'PAS_MAIL_USERS' in os.environ:
    job.attr_mail_list = os.environ['PAS_MAIL_USERS'].strip()

    if logging is True:
        log.write('\n\tMail Users = %s'
                  % (os.environ['PAS_MAIL_USERS']))

if 'PAS_MAIL_OPTIONS' in os.environ:

    if re.match(r"Mail sent at beginning of job", os.environ['PAS_MAIL_OPTIONS']):
        job.attr_mail_options = 'b'
    elif re.match(r"Mail sent at end of job", os.environ['PAS_MAIL_OPTIONS']):
        job.attr_mail_options = 'b'
    elif re.match(r"Mail sent on job abort", os.environ['PAS_MAIL_OPTIONS']):
        job.attr_mail_options = 'a'
    else:
        job.attr_mail_options = 'n'

    if logging is True:
        log.write('\n\tMail Options = %s'
                  % (os.environ['PAS_MAIL_OPTIONS']))

if 'PAS_MAIL_EMAILS' in os.environ:

    if re.match('@', os.environ['PAS_MAIL_EMAILS']):
        job.attr_mail_list = os.environ['PAS_MAIL_EMAILS'].strip()

    if logging is True:
        log.write('\n\tMail Emails = %s'
                  % (os.environ['PAS_MAIL_EMAILS']))

job.attr_additional_attrs = ','.join(attributes)


''' Removing Old Submit Exports '''

files = os.listdir('%s/runtime/' % os.environ['PAS_APP_HOME'])

now = time.time()
cutoff = now - (3 * 86400)

for file in files:

    if os.path.isfile(file):
        if re.match('submit.export.*', file):

            t = os.stat('%s/runtime/%s' % (os.environ['PAS_APP_HOME'], file))
            c = t.st_time

            if c < cutoff:
                os.remove('%s/runtime/%s' % (os.environ['PAS_APP_HOME'], file))

''' Exporting Environment '''

if os.path.exists('%s/runtime/submit.export.%s' % (os.environ['PAS_APP_HOME'], os.environ['PAS_JOB_NAME'])):
    os.remove('%s/runtime/submit.export.%s' % (os.environ['PAS_APP_HOME'], os.environ['PAS_JOB_NAME']))

submit_export = open('%s/runtime/submit.export.%s' % (os.environ['PAS_APP_HOME'], os.environ['PAS_JOB_NAME']), 'a')
os.chmod('%s/runtime/submit.export.%s' % (os.environ['PAS_APP_HOME'], os.environ['PAS_JOB_NAME']), 0755)

for key, value in sorted(os.environ.items()):

    if re.search('PAS_', key):

        if not key.startswith('#'):

            submit_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

    elif re.search('PAS_', value):

        if not key.startswith('#'):

            submit_export.write('%s=%s\n' % (key, value))
            del os.environ[key]

submit_export.close()

if logging is True or logging is True:
    log.close()

sys.stdout.flush()
