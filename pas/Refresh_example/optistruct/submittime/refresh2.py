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
#   Example 2: use case create createArgumentIntEnum, add to the list of arguments at index 3

Debug = True


if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
#1 check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
        options = [1, 2, 3]
        
#  Use case 1 create argument ArgumentIntEnumeratedType add to to position <index>
#  we pass arguments: name, options, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate):

        newArg = refreshUtils.createArgumentIntEnum("NCPU", options, 2, 1, "Number of CPUs", "Number of CPUs", True, False)
#  remove existing element  NCPU
        refreshUtils.deleteApplicationArg("NCPU")
#  add new argument NCPU to the list of arguments, to position index 3
        refreshUtils.addApplicationArg(newArg, 3)
if (Debug == True):
    refreshUtils.printApplicationArgs()




