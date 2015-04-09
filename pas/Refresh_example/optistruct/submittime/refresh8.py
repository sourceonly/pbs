#!/usr/bin/python
# purpose: update job attributes if required
#
# the following objects are available during script execution:
# "applicationArgs": list of arguments (all inputs from user)
# "refreshSourceName": name of the argument, the trigger to run this script on argument value change
# "RefreshUtils" module is available for import;
# refreshUtils can be created: refreshUtils = RefreshUtils.RefreshUtils(applicationArgs)
# it has methods to manipulate application input dynamically(modify, add, delete arguments from user input)

import os, sys

sys.path.append(scriptDir)
import RefreshUtils

#
#   Example 8: use case create ArgumentFileNameMulti, add to the list of arguments

Debug = True

if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
# check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
        options = ["jay3.fem", "jay.fem", "jay1.fem"]
# Use case 8.1 create argument ArgumentFileNameMultiType add to the end of the list
# pass arguments: name, options, separator, defaultValue, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentFileNameMulti("USER_FILES1",  options, ';', "jay3.fem", "user's file", "USER_FILES1", True, False)
#  add new argument to the list of arguments, to the last position
        refreshUtils.addApplicationArg(newArg)
#  Use case 8.2 create argument ArgumentFileNameMultiType add to position 0
# pass arguments: name, options, separator, defaultValue, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentFileNameMulti("USER_FILES2", options, '\n', "jay.fem", "user's file", "USER_FILES2", True, False)
#  add new argument to the list of arguments, to the first position
        refreshUtils.addApplicationArg(newArg, 0)
if (Debug == True):
    refreshUtils.printApplicationArgs()





