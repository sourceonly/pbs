# WARNING: Display Manager(DM) solution is built based on this job script; further customization might not be supported and might break DM

import os, signal, sys
import socket
from time import sleep
from SessionManagerProvider import SessionManagerProvider
from ApplicationManagerProvider import ApplicationManagerProvider
from ConfigurationProvider import ConfigurationProvider
from Util import Util
import logging

#application info holder
class AppInfo:
    pass

appinfo = AppInfo()
appinfo.name = os.environ['PAS_APPLICATION']
appinfo.dmmonhost = os.getenv('PAS_DM_APP_SERVER_MONITOR_HOST')
appinfo.dmmonport = os.getenv('PAS_DM_APP_SERVER_MONITOR_PORT')

#job submission info holder
class JobSumissionInfo:
    pass

jobinfo = JobSumissionInfo()
jobinfo.jobid = os.environ['PBS_JOBID']
jobinfo.appinfo = appinfo

#job submission monitor info
class JobSubmissionMonitorInfo:

    def getHost(self):
        return socket.gethostbyname(jobinfo.appinfo.dmmonhost)

    def getPort(self):
	return int(jobinfo.appinfo.dmmonport)

jobsubmon = JobSubmissionMonitorInfo()

#the main interactive job interface
class InterativeJob:
 
    def __init__(self, session_mgr, app_mgr):

        logging.basicConfig(filename='dmtrace.log', level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        #trap sigterm and terminate the session gracefully
        signal.signal(signal.SIGTERM, self.__terminate)
        self.session_mgr = session_mgr
	self.app_mgr = app_mgr	
	self.config_provider = ConfigurationProvider()
	self.maxtimeout=5*12*30*24*60*60
	self.old_handler=signal.getsignal(signal.SIGALRM)
     
    def run(self):

 	# 1. Update submit
	self.__updateSubmit()
        status=False
	if self.config_provider.get_config('PAS_DM_APP_LAUNCH_STYLE') == "EARLY":
            # 2. Start App With Session
            status = self.app_mgr.start_app(self.config_provider.get_config('PAS_EXECUTABLE'), \
	                           self.config_provider.get_config('PAS_DM_APP_ARGS'), \
                               self.config_provider.get_config('PAS_DM_APP_ENVS'), \
                               self.config_provider.get_config('PAS_DM_APP_WDIR'))
	else:
	    # 2. Start session only
	    status = self.session_mgr.start_session()

        if not status or status is None:
            self.session_mgr.stop_session()
            logging.error('failed to either start app or start session')
            sys.exit(1)
           
	# 3. hold job until either app or session terminates
	self.__holdJob()

	# 4. Update delete
	self.__updateDelete()

    def __updateSubmit(self):
	try:
            sleep(1)
	    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	    self.sock.connect((jobsubmon.getHost(), jobsubmon.getPort()))
	    self.sock.send('command=submit' + '\n' + 'app=' + jobinfo.appinfo.name + '\n' + \
		                'jobid=' + jobinfo.jobid + '\n' + 'server=' + os.getenv('PAS_CLUSTER_NAME')  + '\n')
            logging.info('update this job submit to DM server')
	    self.sock.close()
	except socket.error, (value, msg):
            logging.error(msg)
	    if self.sock:	
	    	self.sock.close()
            sys.exit(1)

    # update DM Server on job delete
    def __updateDelete(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((jobsubmon.getHost(), jobsubmon.getPort()))
            self.sock.send('command=kill' + '\n' + 'jobid=' + jobinfo.jobid + '\n' + \
			'server=' + os.getenv('PAS_CLUSTER_NAME')  + '\n')
            logging.info('update this job delete to DM server')
            self.sock.close()
            util = Util()
            wait = util.getValue("waitOnSession")
            if wait == "Set":
                self.__holdJob()
            else:
                self.session_mgr.stop_session()
  
        except socket.error, (value, msg):
            logging.error(msg)
            if self.sock:
                self.sock.close()
	    sys.exit(1) 	

    # check whether a process exist	
    def __check_pid(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    # read the session expiry timeout value	
    def __readTimeOut(self):
        timeout=self.maxtimeout
        filepath="%s/expiry" %  os.getenv('PBS_JOBDIR')
        if os.path.isfile(filepath):
            file = open(filepath, 'r')
            timeout = file.readline()
            file.close()
        logging.debug('reading the session expiry timer value: %s' %timeout)
        return timeout

    def __expiry_handler(self, signum, frame):
        self.session_mgr.stop_session()

    # hold the job on session pid 	
    def __holdJob(self):
        util = Util()
        session_pid = util.getValue("sessionPid")
        if session_pid is None:
	    return

        ltimeout=self.maxtimeout
        while self.__check_pid(int(session_pid)):
            sleep(1)
            timeout = long(self.__readTimeOut())
            if timeout == ltimeout:
                continue
            if timeout == 0:
        	logging.info('disable session expiry timer')
                signal.signal(signal.SIGALRM, self.old_handler)
                signal.alarm(0)
            else:
        	logging.info('reset session expiry timer from %(f)d to %(t)d' % {'f':ltimeout, 't':timeout})
                signal.signal(signal.SIGALRM, self.__expiry_handler)
                signal.alarm(timeout)
            ltimeout = timeout

        signal.signal(signal.SIGALRM, self.old_handler)
        signal.alarm(0)
        sleep(2)

    def __terminate(self, signum, frame):
	self.__updateDelete()
	sys.exit(1)

#main 	
config_provider = ConfigurationProvider()

sessionmgr_provider = SessionManagerProvider()
sessionmgr = sessionmgr_provider.get_session_mgr(config_provider.get_config('DM_SESSION_MGR'))

appmgr_provider = ApplicationManagerProvider()
appmgr = appmgr_provider.get_app_mgr(config_provider.get_config('DM_APP_MGR'))

job = InterativeJob(sessionmgr, appmgr)
job.run()
sys.exit(0)
