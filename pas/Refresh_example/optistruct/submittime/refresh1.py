#!/usr/bin/python
# purpose: update job attributes if required
#
# the following objects are available during script execution:
# "applicationArgs": list of arguments (all inputs from user)
# "refreshSourceName": name of the argument, the trigger to run this script on argument value change
# "RefreshUtils" module is available for import;
# refreshUtils can be created: refreshUtils = RefreshUtils.RefreshUtils(applicationArgs)
# it has methods to manipulate application input dynamically(modify, add, delete arguments from user input)
import sys
import os
sys.path.append(scriptDir)
import RefreshUtils

#
##   Example 1: use case of create ArgumentInt, add to the list of arguments at index 6

Debug = True

if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
    refreshUtils.printApplicationArgs()
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
#1 check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
#     create argument ArgumentIntType
#     we pass arguments: name, value, defaultValue, description, displayName, inputRequired, refreshOnUpdate):
    if(version == "11.0"):
        newArg = refreshUtils.createArgumentInt("ADDITIONAL_SOLVER_OPTION", 2, 1, "Descr: additional solver option, integer", "ADDITIONAL_SOLVER_OPTION", True, False)
    #     add argument to the list of arguments, to position index 6
        refreshUtils.addApplicationArg(newArg, 6)

if (refreshSourceName == "ZIP_RESULTS"):
    zipresults = refreshUtils.getFeatureEnabled("ZIP_RESULTS")
if (Debug == True):
    refreshUtils.printApplicationArgs()
    print str(env)
    print str(policies)




