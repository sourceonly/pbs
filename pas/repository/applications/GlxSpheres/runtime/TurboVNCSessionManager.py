import subprocess
import logging
import sys
import socket
import os
import re
import Constants
from ConfigurationProvider import ConfigurationProvider
from Util import Util

#TurboVNC implementation to start, stop sessions
class TurboVNCSessionManager:

    def __init__(self):
        logging.basicConfig(filename='dmtrace.log', level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def start_session(self):

        logging.info('starting display server')
	configmgr = ConfigurationProvider()
	geometry = configmgr.get_config('PAS_DM_APP_GEOMETRY')
        cmd="%(vncpath)svncserver -geometry %(geo)s -novncauth -nopam" % {'vncpath':Constants.TurboVNC_EXEC_PATH, 'geo':geometry}
 	logging.info('executing cmd %(cmd)s' % {'cmd':cmd})
        vncstart = subprocess.Popen(re.split(' ', cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	out, err = vncstart.communicate() 
        if vncstart.returncode != 0:
            logging.error('display server failed to start with error %s' % err)
            sys.stderr.write(err)
        else:
            self.__update(err, geometry)
            util = Util()
        return util.getValue("display")

    def __update(self, vncoutput, geometry):

        status = False 
        for token in vncoutput.split("\n"):
            m = re.search('Desktop', token, re.IGNORECASE)
            if m: 
	        display = re.search('\d+', re.split(':',token)[-1]).group()
                status = True

        if not status:
            return status

        cmd=['ps', '-eaf']
        ps = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        out, err = ps.communicate()
        logging.info('display %s' %display)
        status=False
	for item in out.split("\n"):
            m = re.search('Xvnc', item, re.IGNORECASE)
            if m:
                str = "%(h)s:%(d)s" %{'h':socket.gethostname(), 'd':display}
                m = re.search(str, item, re.IGNORECASE)
                if m:
                    entries=re.split('\s+', item.strip())
        	    pid = entries[1]
        	    idx=0
        	    for entry in entries:
          	        if entry == "-rfbport":
              		    port=entries[idx+1]
                            status = True 
              	    	    break
          	        idx+=1;
        	    break

        if status:
            output = "display=:%(d)s\ngeometry=%(geo)s\nhost=%(host)s\nport=%(port)s\nsessionPid=%(pid)s\n" \
                        % {'d':display, 'geo':geometry, 'host':socket.gethostname(), 'port':port, 'pid':pid}
            logging.info('display server started successfully: %s' % output)
	    util = Util()
	    util.createDMInfo(output)	
        else:
            logging.error('failed to update session information')
            sys.stderr.write('failed to update session information')
        return status

    def stop_session(self):

        status = False
        util = Util()
        display = util.getValue("display")
	if display is not None:
            logging.info('stopping display %s' % display)
            logging.debug('ENVS: %s' % os.environ)
            cmd="%(vncpath)svncserver -kill %(d)s" % {'vncpath':Constants.TurboVNC_EXEC_PATH, 'd':display}
            logging.info('executing cmd %(cmd)s' % {'cmd':cmd})
            vnckill = subprocess.Popen(re.split(' ', cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    close_fds=True)
	    out, err = vnckill.communicate()
            if vnckill.returncode != 0:
                logging.error('display stop failed with error %s' % err)
                sys.stderr.write(err)
            else:
                util.removeDMInfo()
                logging.info("display stopped successfully")
                status = True
        return status 

    def gen_password(self):

        status = False
	util = Util()
	display = util.getValue("display")
        logging.info('generating password for display %s' % display)
        logging.debug('ENVS: %s' % os.environ)
        cmd="%(vncpath)svncpasswd -o -display %(d)s" % {'vncpath':Constants.TurboVNC_EXEC_PATH, 'd':display}
        logging.info('executing cmd %(cmd)s' % {'cmd':cmd})
        vncpassword = subprocess.Popen(re.split(' ', cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    close_fds=True)
        out, err = vncpassword.communicate()
        if vncpassword.returncode != 0:
            logging.error('password generation failed with error %s' % err)
            sys.stderr.write(err)
        else:
            logging.info("password generation successful")
	    out=re.split(' ', err)[4]
            sys.stdout.write(out)
            sys.stdout.flush()
            status = True
        return status

    def get_session(self):
        util = Util()
        return util.getDMInfo()
        
    def set_waitflag(self):

	util = Util()
        logging.info('setting the wait on session flag')
	return util.update("waitOnSession", "Set")

    def set_expiry(self, timeout):

        status = False
        logging.info('setting the session expiry timer')
        logging.debug('ENVS: %s' % os.environ)
        configmgr = ConfigurationProvider()
        jobdir = configmgr.get_config("PBS_JOBDIR")
        if timeout is not None:
            filepath="%s/expiry" % jobdir
            file = open(filepath, 'w+')
            os.chmod(filepath, 0644)
            file.write("%s" %timeout)
            file.flush()
            file.close()
            logging.info('session expiry timer updated to: %s' %timeout)
            status = True
        else:
            logging.error('session expiry timer update failed')
        return status

