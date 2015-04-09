#coding: utf-8

'''
© Copyright 2013 - 2014 Altair Engineering, Inc. All rights reserved.
This code is provided “as is” without any warranty, express or implied, or
indemnification of any kind. All other terms and conditions are as specified
in the Altair PBS Application Services EULA.
'''

import pbs
import os

__version__ = '12.1.0'

job = pbs.event().job

if 'PAS_APPLICATION' in job.Variable_List:

    ''' Importing Environment '''

    for key, value in job.Variable_List.items():
        os.environ[key.strip()] = value.strip()

    if 'PAS_ENVIRONMENT' in os.environ:

        for variable in os.environ['PAS_ENVIRONMENT'].split(';'):

            if re.match('(.*)=(.*)', variable):

                if not variable.startswith('#'):

                    (key, value) = variable.split('=', 1)
                    os.environ[key.strip()] = value.strip()

        del os.environ['PAS_ENVIRONMENT']

    if 'PAS_SUBMISSION_DIRECTORY' in os.environ:

        elements = os.environ['PAS_SUBMISSION_DIRECTORY'].split('/', 3)
        os.environ['PAS_USER_STAGE'] = elements[3].strip()
        os.chdir('/%s' % (os.environ['PAS_USER_STAGE']))

    ''' Logging '''

    log = open('submit.log', 'a')

    logging = False

    if 'PAS_LOGGING' in os.environ:

        if os.environ['PAS_LOGGING'] == 'true':
            logging = True
        elif os.environ['PAS_LOGGING'] == 'false':
            logging = False

    ''' Input File Array '''

    if 'PAS_INPUT_FILE_ARRAY' in os.environ:

        if logging is True:
            log.write('\n\nFound Input File Array\n')

        array_size = len(os.environ['PAS_INPUT_FILE_ARRAY'].split(';'))

        if array_size == 1:

            if logging is True:
                log.write('\n\tFound a single input file. This will be a typical batch job.')

            pbs.event().accept()

        elif array_size >= 2:

            if logging is True:
                log.write('\n\tFound multiple input files. This will be an array of jobs.')

            job.array_indices_submitted = pbs.range("1-%d" % array_size)
            pbs.event().accept()

        else:
            pbs.event().reject()

    #''' Depend by Name '''
    #
    #if 'PAS_DEPEND_BY_NAME' in os.environ:
    #    '''
    #    '''

    log.close()

    ''' Clean Up Environment '''

    for key, value in sorted(os.environ.items()):

        if re.search('PAS_', key):
            del os.environ[key]

        elif re.search('PAS_', value):
            del os.environ[key]

pbs.event().accept()
