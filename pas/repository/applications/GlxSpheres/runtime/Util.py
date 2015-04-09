from ConfigurationProvider import ConfigurationProvider
import logging
import os
import sys
from time import sleep

# Utility that helps lookup DM information file
class Util:
    def getValue(self, var):
        configmgr = ConfigurationProvider()
        jobdir = configmgr.get_config("PBS_JOBDIR")
 	filepath="%s/dm.info" % jobdir
        value = None
	if os.path.isfile(filepath):
            file = open(filepath, 'r')
            for entry in file.readlines():
                splitwords = entry.split("=")
                if var == splitwords[0]:
                    value = splitwords[1].replace("\n", "")
	            logging.info('Found key= %(key)s value=%(val)s' % {'key':var, 'val':value})
		    break
	        file.close()
        return value

    def update(self, key, value):
        status = False
        configmgr = ConfigurationProvider()
        jobdir = configmgr.get_config("PBS_JOBDIR")
        filepath="%s/dm.info" % jobdir
        if os.path.isfile(filepath):
            file = open(filepath, 'a')
            output="%(key)s=%(val)s\n" \
                        % {'key': key, 'val': value}
	    logging.info("Updated %s" %output)
            file.write(output)
            file.flush()
            file.close()
            status = True
        else:
            logging.error('file %s does not exist' %filepath)
            sys.stderr.write('file %s does not exist' %filepath)
        return status

    def removeDMInfo(self):
        status = False
        configmgr = ConfigurationProvider()
        jobdir = configmgr.get_config("PBS_JOBDIR")
        filepath="%s/dm.info" % jobdir
        if os.path.isfile(filepath):
	    os.remove(filepath)	
            logging.info("removed DM info file %s" %filepath)
            status = True
        else:
            logging.error('file %s does not exist' %filepath)
            sys.stderr.write('file %s does not exist' %filepath)
        return status

    def getDMInfo(self):
        status = False
        configmgr = ConfigurationProvider()
        logging.info('getting the session information')
        logging.debug('ENVS: %s' % os.environ)
        jobdir = configmgr.get_config("PBS_JOBDIR")
        filepath="%s/dm.info" % jobdir
        counter = 5
        while ((not os.path.exists(filepath)) and (counter>0)):
            sleep(0.5)
            counter -= 1
        if os.path.isfile(filepath):
            file = open(filepath, 'r')
            sessionout = file.read()
            logging.info('session output %s' % sessionout)
            sys.stdout.write(sessionout)
            sys.stdout.flush()
            file.close()
            status = True
        else:
            logging.error('file %s does not exist' %filepath)
            sys.stderr.write('file %s does not exist' %filepath)
        return status

    def createDMInfo(self, info):
       configmgr = ConfigurationProvider()
       jobdir = configmgr.get_config("PBS_JOBDIR")
       file = open("%s/dm.info" % jobdir, 'w+')
       file.write(info)
       file.flush()
       file.close()

