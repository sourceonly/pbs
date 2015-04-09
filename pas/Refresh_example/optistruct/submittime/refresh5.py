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
#   Example 5: use case create ArgumentStringEnum, add to the list of arguments

Debug = True

#def printApplicationArgs():
#    if(Debug):
#
#        print>> sys.stdout,("refreshSourceName : %s") % refreshSourceName
#        print>> sys.stdout,("applicationArgs.size(): %s") % str(applicationArgs.size())
#    for arg in applicationArgs:
#        try:
#            print str(arg.name)
#
#        except OSError, err:
#            print >> sys.stderr, str(err)
#    sys.stdout.flush()
#    sys.stderr.flush()

if (Debug == True):
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)
#    refreshUtils.printApplicationArgs()
else:
    refreshUtils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName)
#1 check the refreshSourceName
if(refreshSourceName == "VERSION"):
    version = refreshUtils.getValue("VERSION")
    if(version == "11.0"):
        options = ["RESOURCE1", "RESOURCE2", "RESOURCE3"]
        
# Use case 5.1 create argument ArgumentStringEnumeratedType add to the end of the list
#    pass arguments: name, options, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentStringEnum("TEST_STRING_ENUM1", options,  "RESOURCE1", "RESOURCE1", "string enum", "TEST_STRING_ENUM1", True, False)
#  add new argument TEST_STRING_MULTI1 to the list of arguments, to the last position
        refreshUtils.addApplicationArg(newArg)
#  Use case 5.2 create argument ArgumentStringEnumeratedType add to position 0
#  pass arguments: name, options, val, defaultValue, description, displayName, inputRequired, refreshOnUpdate
        newArg = refreshUtils.createArgumentStringEnum("TEST_STRING_ENUM2", options, "RESOURCE1","RESOURCE1", "string enum", "TEST_STRING_ENUM2", True, False)
#  add new argument TEST_STRING_MULTI2 to the list of arguments, to the first position
        refreshUtils.addApplicationArg(newArg, 0)
refreshUtils.printApplicationArgs()
# additional logic here




