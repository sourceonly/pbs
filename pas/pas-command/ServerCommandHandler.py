#!/usr/bin/python
# -*- coding: "UTF-8" -*-

import os
import sys
import CommonUtils
import HelpGenerator

class ServerCommandHandler:


    def handleRequest(self):
        if 'ping' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('ping')    
                help.displayHelp()
                sys.exit(0)
            self.ping()
            
        elif 'isadmin' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('isadmin')    
                help.displayHelp()
                sys.exit(0)
            self.isadmin()
            
        elif 'get-pas-version' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('get-pas-version')    
                help.displayHelp()
                sys.exit(0)
            self.pas_version()

        elif 'get-stage-root' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('get-stage-root')    
                help.displayHelp()
                sys.exit(0)
            self.getSRoot()

        elif 'get-default-server' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('get-default-server')    
                help.displayHelp()
                sys.exit(0)
            self.getServer()

        elif 'pas-password' in self.opts.keys():
            if (self.opts['commandHelp'] == True):
                help = HelpGenerator.HelpGenerator('pas-password')    
                help.displayHelp()
                sys.exit(0)
            self.setPassword()            

        elif 'help' in self.opts.keys():
            self.displayHelp()

                 
    def __init__(self, opts):        
        self.opts = opts.__dict__
        if (('pasServer' in self.opts.keys()) and (self.opts['pasServer'] != None)):
            CommonUtils.pas_server = self.opts['pasServer']
            
        self.handleRequest()


    def ping(self):
        import JobManager
        import ServerStatus
        import socket

        try:
            if(self.opts['verbose'] == True):
                serverStatusObj = ServerStatus.ServerStatus()
                serverStatusObj.displayServerStatus(self.opts['verbose'])
            else:
                jobMgr = JobManager.JobManager()
                jobMgr.pingServer()
        except socket.timeout,msg:
            print >>sys.stderr, msg
            sys.exit(106)
        except ServerStatus.PASServerDown,msg:
            print >>sys.stderr,msg
            sys.exit(106)
        except ServerStatus.ServerNotPinging,msg:
            print >>sys.stderr,msg
            sys.exit(106)
        except JobManager.PasServerError, (err):
            print >>sys.stderr, ("ERROR: PAS Server error: \n%s")%(err)        
            sys.exit(107)    
        except Exception, (err):
            print >>sys.stderr, ("ERROR: Error in ping PAS server \n%s")%(err)
            if err.find("FailedLoginException:") >= 0:
                print>>sys.stdout, ("\nPlease run pas-passwd command to set the password for pas-client user")
            sys.exit(106)

    def isadmin(self):
        import ServerStatus

        try:
            if(('pasServer' in self.opts.keys()) and (self.opts['pasServer'] == None) and (len(sys.argv) > 2)):
                print >>sys.stdout, ("Invalid command")
                sys.exit(102)
            serverStatusObj = ServerStatus.ServerStatus()
            isAdmin = serverStatusObj.isAdmin(self.opts['pasServer'])
            print >>sys.stdout, isAdmin
        except ServerStatus.PasServerError, err:
            print >>sys.stderr, ("ERROR: PAS server error: \n%s")%(err)
            if err.find("FailedLoginException:") >= 0:
                print>>sys.stdout, ("\nPlease run pas-passwd command to set the password for pas-client user")
            sys.exit(107)
        except Exception, (err):
            print >>sys.stderr, ("ERROR: Error in is admin \n%s")%(err)
            sys.exit(111)

    def pas_version(self):
        import ServerStatus
    
        try:
            if(('pasServer' in self.opts.keys()) and (self.opts['pasServer'] == None) and (len(sys.argv) > 2)):
                print >>sys.stdout, ("Invalid command")
                sys.exit(102)     
            serverStatusObj = ServerStatus.ServerStatus()
            serverStatusObj.displayServerVersion()        
        except Exception, (err):
            print >>sys.stderr, ("ERROR: Error in get PAS version \n%s")%(err)
            sys.exit(111)

    def getSRoot(self):
        import FileManager

        try:
            if(('pasServer' in self.opts.keys()) and (self.opts['pasServer'] == None) and (len(sys.argv) > 2)):
                print >>sys.stdout, ("Invalid command")
                sys.exit(102)        
            fileMgr = FileManager.FileManager()
            stageRoot = fileMgr.getStageRoot()
            print >> sys.stdout, ("%s")%(stageRoot)
        except FileManager.PASServerError, err:
            print >>sys.stderr, ("ERROR: PAS server error \n%s")%(err)
            if str(err).find("FailedLoginException:") >= 0:
                    print>>sys.stderr, ("\nPlease run pas-passwd command to set the password for pas-client user")
            sys.exit(107)
        except Exception, (err):
            print >>sys.stderr, ("ERROR: Error in get stage root \n%s")%(err)
            sys.exit(111)

    def getServer(self):
        import ConfigurationUtils
    
        try:
            config = ConfigurationUtils.ConfigurationUtils()
            config.displayDefaultServer()
        except ConfigurationUtils.DefaultServerNotFound, (err):
            print >>sys.stderr, ("ERROR: Default server not found. Use (pas-setsrv) to register a server: \n%s")%(err)
            sys.exit(109)    
        except Exception, (err):
            print >>sys.stderr, ("ERROR: Error in get default server \n%s")%(err)
            sys.exit(111)

    def passwordReader(self):
        import getpass
	import sys
	if not sys.stdin.isatty(): 
		return sys.stdin.readline().rstrip();
        pprompt = lambda: (getpass.getpass('Enter user\'s password:'), getpass.getpass('Retype password: '))
        str1, str2 = pprompt()

        while str1 != str2:
            print >>sys.stdout, ("Passwords do not match.")        
            input = str(raw_input("Try Again (Y/N)")).strip()        
            if input == str("Y") or input == str("y"):
                str1, str2 = pprompt()
            else:
                exit(0)
        return  str1

    def setPassword(self):
        import PasswordManager
        import ConfigurationUtils
        import getpass
        
        try:            
            str = self.passwordReader()
            pwdObj = PasswordManager.PasswordManager()
            pwdObj.savePassword(str)
            print >>sys.stdout,("Changed user %s's PAS password on server <%s>")%(getpass.getuser(),ConfigurationUtils.ConfigurationUtils().getServer())
        except KeyboardInterrupt:
            print >>sys.stderr, ("\n Keyboard interrupt")
            sys.exit()
        except Exception:
            print >>sys.stderr, ("Invalid Operation")
            sys.exit()


    def displayHelp(self):
        print "These commands are used to execute PAS functionality\n\n"
        print "\tpas-help\tTo view list of available commands"
        print "\tpas-ping\tPing PAS server"
        print "\tpas-getsrv\tDisplay information about default server"
        print "\tpas-getapp\tGets the job submission parameters of the application"
        print "\tpas-getapps\tGets the list of applications registered on PAS server"
        print "\tpas-submit\tSubmit the job on PAS"
        print "\tpas-getres\tDownload job result for specified job id"
        print "\tpas-stat\tChecks the status of given job"
        print "\tpas-fdown\tDownloads files from the PAS server"
        print "\tpas-flist\tList files for the given directory"
        print "\tpas-sum \tDisplay summary of given jobId"
        print "\tpas-ver \tGives PAS version and build information"
        print "\tpas-del \tTerminates the job from PBS"
        print "\tpas-fup \tUploads file on PAS server"
        print "\tpas-fmkdir\tCreates directory on PAS server"
        print "\tpas-fdel\tDelete file from the given path"
        print "\tpas-fcompr\tCompress file from the given path"
        print "\tpas-getsroot\tGet the stage directory"
        print "\tpas-admin\tChecks whether logged in user is admin or not"
        print "\tpas-passwd\tSet the password of logged in user"

        
#######MAIN########
'''           
argv = sys.argv[1]            
str1 = ((((argv.replace("{","")).replace("}","")).replace("'", "")).replace(":",",")).replace(" ","")
list1 = str1.split(",")
opts = dict([(k, v) for k,v in zip (list1[::2], list1[1::2])])

serverCmdHndlr = ServerCommandHandler(opts)
'''



                                                
