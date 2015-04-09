import subprocess
import sys
import os
import logging
import string
import re

from TurboVNCSessionManager import TurboVNCSessionManager
from ConfigurationProvider import ConfigurationProvider
import Constants
from Util import Util

# VGL implementation to start/stop an application
class VGLApplicationManager:

    def __init__(self):
        logging.basicConfig(filename='dmtrace.log', level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def __check_X_access(self, resource):

        status = 0
        if resource is not None:
            logging.info('checking X server access')
	    cmd = "%(vglpath)sglxinfo -display %(d)s -c" % {'vglpath':Constants.VGL_EXEC_PATH, 'd':resource}
            logging.info('executing cmd %(cmd)s' % {'cmd':cmd})
            glxinfo = subprocess.Popen(re.split(' ', cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	    out, err = glxinfo.communicate()
            status = glxinfo.returncode
	    if status != 0:
	        logging.error('access to X server is not granted on display %(r)s with err %(e)s' % {'r':resource, 'e':err})
                sys.stderr.write(err)
            else:
                logging.info('access to X server is granted')
                logging.debug('%s' % out)
        return status


    def __getRes(self):

	resource = None
        configmgr = ConfigurationProvider()
        jobdir = configmgr.get_config("PBS_JOBDIR")
	filepath="%s/resource" % jobdir
	if os.path.isfile(filepath):
	    file = open(filepath, 'r')
            filec=file.readline()
	    logging.info("reading resource file %(o)s" % {'o':filec})
	    splitwords = filec.split(":")
	    # Format :<display>.<screen>
 	    resource = ":0.%s" % splitwords[1]
	    resource = resource.rstrip('\n')
            file.close()
	return resource

    def __updateEnvs(self, envs):

	if envs is not None:
	    for entry in envs.split("\n"):
		logging.debug('env line %(l)s' % {'l':entry})
	        splitwords = entry.split("=")
	        var = splitwords[0]
                val = splitwords[1]
	        logging.debug('updating env var %(var)s val %(val)s' % {'var':var, 'val':val})	
                os.environ[var] = val

    def start_app(self, cmd, args=None, envs=None, cwd=None, display=None):

        sessionmgr = TurboVNCSessionManager()
	configmgr = ConfigurationProvider()

	# Get the allocated GPU resource
        resource = self.__getRes()
	logging.info("GPU resource id =%(res)s" % {'res':resource})	

        # Validate X access as the first thing for OpenGL apps
        if self.__check_X_access(resource) != 0:
	    return False
	
        # Start a new TurboVNC server if required
        if display is None:
            display = sessionmgr.start_session()
            if display is None:
                return False

	# Update the process envs
	self.__updateEnvs(envs)

        # Set the DISPLAY environment
        os.environ['DISPLAY'] = display
	envs = os.environ.copy()

        if cwd is None:
            cwd = configmgr.get_config("PBS_JOBDIR")
	     			
	if resource is not None:
	    cmd = "%(vglpath)svglrun -d %(d)s -sp %(cmd)s" % {'vglpath':Constants.VGL_EXEC_PATH, 'd':resource, 'cmd':cmd}
        
	if args is not None:
            cmd = '%(c)s %(a)s' % {'c':cmd, 'a':args}

	    # Start the application on a given display {use VGL for OpenGL}
        logging.info("starting application exec=%(cmd)s envs=%(envs)s cwd=%(cwd)s display=%(d)s" \
                                 % {'cmd':cmd, 'envs':envs, 'cwd':cwd, 'd':display})
       
        appname = configmgr.get_config('PAS_APPLICATION')
        app = subprocess.Popen(re.split(' ', cmd), env=envs, cwd=cwd, shell=False, \
				   stdout=open('%s.STDOUT'%appname, 'w'), \
          		         stderr=open('%s.STDERR'%appname, 'w'), close_fds=True)

        util = Util()
        util.update("appPid", app.pid)
        return True

