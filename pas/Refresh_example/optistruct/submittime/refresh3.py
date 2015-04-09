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
#   Example 3: use case create createArgumentIntEnum, add to the list of arguments at index 3

Debug = True

if (Debug == False):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
#1 check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
        options = [1, 2, 3]
        
#  Use case 3.1 create argument ArgumentStringType add to the last position
#  pass arguments: name, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate:
        newArg = refreshUtils.createArgumentString("TEST_STRING_RES1", "VAL1", "VAL2", "string argument", "TEST_STRING_RES1", True, False)
#  add new argument  to the list of arguments, to the last position
        refreshUtils.addApplicationArg(newArg)
#  Use case 3.2  create argument ArgumentStringType add to the <index> position
#  pass arguments: name, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate:
        newArg = refreshUtils.createArgumentString("TEST_STRING_RES2", "VAL2", "VAL2", "string argument", "TEST_STRING_RES2", True, False)
#  add new argument to the list of arguments, to the first position
        refreshUtils.addApplicationArg(newArg, 0)
if (Debug == True):
    refreshUtils.printApplicationArgs()




