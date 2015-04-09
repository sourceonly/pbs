import os, sys
import subprocess

sys.path.append(scriptDir)
import RefreshUtils
import Utils

Debug = True
if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
# check the refreshSourceName
new_queue_options = []
if(refreshSourceName == None):
    command_qmgr = 'qmgr'

    utils = Utils.Utils()
    if utils.is_platform_windows():
        # on windows path to gmgr needs to be added to the global PATH
        utils.set_comspec()
        utils.add_pbsbin_path()
    else:
        # on UNIX we need to construct full path to qmgr
        command_qmgr = utils.get_pbs_bin() + '/' + command_qmgr
	command_to_str = command_qmgr + ' ' + '-c ' + ' ' + str(["p s"]).strip('[]')
	try:
		rcp=subprocess.Popen([ command_qmgr ] + ['-c'] + ["p s"], shell=False, stdin=None, stdout=subprocess.PIPE, bufsize=-1, stderr=None)
		line=rcp.stdout.readline()
		while ( line ) :
			if line.find("create queue") != -1:
				queue_name = ""
				startIndex = (len("create queue"))+1
				endIndex = len(line)
				queue_name = line[startIndex : endIndex].rstrip()
				new_queue_options.append(queue_name)

			line=rcp.stdout.readline() #drain stdin even if job_history status is already detected
	except IOError:
		exitcode=106
		print >> sys.stderr, ('exitcode: %d. IOError happened while executing command : %s')% (exitcode, command_to_str)
		sys.exit(exitcode)
	except OSError, err:
		exitcode=106
		print >> sys.stderr, ('exitcode: %d. System Error happened while executing command : %s')% (exitcode, command_to_str)
		sys.exit(exitcode)
	if(len(new_queue_options)>0):
		newArg = refreshUtils.createArgumentStringEnum("QUEUE", new_queue_options,  new_queue_options[0], new_queue_options[0],"queues enum", "queues", True, False)
#  add new argument QUEUE to the list of arguments, to the last position
		refreshUtils.addApplicationArg(newArg)
    
elif(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
# Use case 9.1 create argument ArgumentBooleanWithDescription add to the end of the list
# pass arguments: name, featureEnabled, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentBooleanWithDescription("TEST_BOOLEAN1",  True, "argument, boolean type", "argument, boolean type", True, False)
#  add new argument to the list of arguments, to the last position
        refreshUtils.addApplicationArg(newArg)
#  Use case 9.2 create argument ArgumentBooleanWithDescription add to position 0
# pass arguments: name, featureEnabled, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentBooleanWithDescription("TEST_BOOLEAN2", False, "argument, boolean type", "argument, boolean type", True, False)
#  add new argument to the list of arguments, to the first position
        refreshUtils.addApplicationArg(newArg, 0)
if (Debug == True):
    refreshUtils.printApplicationArgs()

sys.stdout.flush()
sys.stderr.flush()


