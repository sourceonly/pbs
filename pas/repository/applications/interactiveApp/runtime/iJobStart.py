import os, signal, sys
import socket
import subprocess
from time import sleep
from subprocess import call
import commands

#application info holder
class AppInfo:
    pass

appinfo = AppInfo()
appinfo.name = os.environ['PAS_APP_NAME']
appinfo.version  = os.getenv('PAS_APP_VER', 'default')
appinfo.geometry = os.environ['PAS_APP_GEOMETRY']
appinfo.args = os.getenv('PAS_APP_ARG', 'None')
appinfo.envs = os.getenv('PAS_APP_ENV', 'None')
appinfo.startdir = os.getenv('PAS_START_DIR', 'None')
appinfo.gpu = os.getenv('PAS_GPU', 'None')
appinfo.dmserver = os.getenv('PAS_DM_APP_SERVER', 'NOT_SET')

#job submission info holder
class JobSumissionInfo:
    pass

jobinfo = JobSumissionInfo()
jobinfo.user = os.environ['AIF_USER']
jobinfo.host = os.environ['HOSTNAME']
jobinfo.jobid = os.environ['PBS_JOBID']
jobinfo.jobdir = os.environ['PBS_JOBDIR']
jobinfo.jobname = os.getenv('PAS_JOB_NAME', 'NOT_SET')
jobinfo.appinfo = appinfo

#job submission monitor info
class JobSubmissionMonitorInfo:

    def getHost(self):
        if (jobinfo.appinfo.dmserver != "NOT_SET"):
                return jobinfo.appinfo.dmserver
        else:
                retVal = self.__getVal("JOB_SUBMISSION_MONITOR_HOST")
                if ( retVal == "failed" ):
                        return socket.gethostbyname(os.environ['PBS_O_HOST'])
                return socket.gethostbyname(retVal)

    def getPort(self):
        retVal = self.__getVal("JOB_SUBMISSION_MONITOR_PORT")
	if ( retVal == "failed" ):
		return 4909
	return int(retVal)

    def __getVal(self, input):

        filepath = "runtime/ijob.conf"
        if (os.path.exists(filepath)):
                configfile = open(filepath, "r")
                found = "false"
                while True:
                        line = configfile.readline()
                        if len (line) == 0:
                                return "failed"

                        words=line.split("=")
                        for seq in words:
                                if (found == "true"):
                                        return seq.strip()

                                if ( seq == input):
                                        found="true"
	else:
		return "failed"	

	
jobsubmon = JobSubmissionMonitorInfo()

#the main interactive job interface
class InterativeJob:
      
    def __init__(self, jobinfo):
	
	#trap sigterm and terminate the session gracefully
	signal.signal(signal.SIGTERM, self.__terminate)

    def run(self):

	self.__writejobid()
	self.__update()

	try:
	    pidfile = os.environ['PBS_JOBDIR'] + "/jobpid"
	    counter = 5;

	    #wait until the pid (session) is available.. timeout after 5 secs
	    while ((not os.path.exists(pidfile)) and (counter > 0)):
  	        sleep(1)
	        counter -= 1
	
	    if counter > 0:	
  	       f = open(pidfile)
	       self.pid = f.readline()

	       #if pid is available within 5 secs, wait until the pid becomes unavailable
	       while self.__check_pid(int(self.pid)):
	           sleep(0.5)	

	       f.close()
  	       os.unlink(pidfile) 
	
	except IOError:
	    sys.stderr.write("cannot open %s" % pidfile)
	    sys.exit(1)

    def __check_pid(self, pid):        
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True
		
    def __update(self):

	try:
	    sleep(0.5)
	    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	    self.sock.connect((jobsubmon.getHost(), jobsubmon.getPort()))

	    self.sock.send('command=submit' + '\n' + 'host=' + jobinfo.host + '\n' + 'jobdir=' + jobinfo.jobdir + '\n' + \
		'user=' + jobinfo.user + '\n' + 'jobid=' + jobinfo.jobid + '\n' + 'jobname=' + jobinfo.jobname + '\n' + \
		'app_name=' + jobinfo.appinfo.name + '\n' + 'app_ver=' + jobinfo.appinfo.version + '\n' + 'app_args=' + jobinfo.appinfo.args + '\n' + \
		'app_envs=' + jobinfo.appinfo.envs + '\n' + 'app_startdir=' + jobinfo.appinfo.startdir + '\n' + \
		'app_geometry=' + jobinfo.appinfo.geometry + '\n' + 'gpu=' + jobinfo.appinfo.gpu + '\n')
 
	    self.sock.close()
	except socket.error, (value, msg):
            sys.stderr.write(msg)
	    if self.sock:	
	    	self.sock.close()

            sys.exit(1)

    def __writejobid(self):
	
	try:
           jobidfp = os.environ['PBS_JOBDIR'] + "/jobid"
           jobidf = open(jobidfp, 'w')
           jobidf.write(jobinfo.jobid)
           jobidf.close()
	except IOError:
            sys.stderr.write("cannot open %s" % jobidfp)
            sys.exit(1)
	 	
    def __terminate(self, signum, frame):

	    pidfile = os.environ['PBS_JOBDIR'] + "/jobpid"

	    if os.path.exists(pidfile):
	
        	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            	self.sock.connect((jobsubmon.getHost(), jobsubmon.getPort()))
            	self.sock.send('command=kill' + '\n' + 'user=' + jobinfo.user + '\n' + 'jobid=' + jobinfo.jobid + '\n')
            	self.sock.close()

	    sys.exit(1) 	

#main 	
job = InterativeJob(jobinfo)
job.run()

