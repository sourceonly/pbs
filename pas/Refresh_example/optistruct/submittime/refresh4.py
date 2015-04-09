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
#   Example 4: use case create ArgumentStringMultiType, add to the list of arguments

Debug = True

if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
# check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
        options = ["RESOURCE1", "RESOURCE2", "RESOURCE3"]
        
# Use case 4.1 create argument ArgumentStringMultiType separated with ';'
#    pass arguments: self, name, options, separator, defaultValue, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentStringMulti("TEST_STRING_MULTI1", options, ';', "RESOURCE1", "string multi separated with \';\'", "TEST_STRING_MULTI1", True, False)
#  add new argument TEST_STRING_MULTI1 to the list of arguments, to the last position
        refreshUtils.addApplicationArg(newArg)
#  Use case 4.2 create argument ArgumentStringMultiType separated with new line
#  pass arguments: name, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate:
        newArg = refreshUtils.createArgumentStringMulti("TEST_STRING_MULTI2", options, '\n', "RESOURCE1","string multi each on new line", "TEST_STRING_MULTI2", True, False)
#  add new argument TEST_STRING_MULTI2 to the list of arguments, to the first position
        refreshUtils.addApplicationArg(newArg, 0)
if (Debug == True):
        refreshUtils.printApplicationArgs()




