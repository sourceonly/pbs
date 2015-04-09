# WARNING: Display Manager(DM) solution is built based on this custom action script; further customization might not be supported and might break DM

import os
import sys
 
sys.path.append(os.getcwd()+"/runtime")

from SessionManagerProvider import SessionManagerProvider
from ConfigurationProvider import ConfigurationProvider
from ApplicationManagerProvider import ApplicationManagerProvider
from Util import Util

config_provider = ConfigurationProvider()
appmgr_provider = ApplicationManagerProvider()
appmgr = appmgr_provider.get_app_mgr(config_provider.get_config('DM_APP_MGR'))

sessionmgr_provider = SessionManagerProvider()
sessionmgr = sessionmgr_provider.get_session_mgr(config_provider.get_config('DM_SESSION_MGR'))

util = Util()

status = False
action = os.environ['PAS_ACTION_DM_CUSTOM_ACTION_TYPE']
if action == "START_APP":
    status=appmgr.start_app(config_provider.get_config('PAS_EXECUTABLE'), config_provider.get_config('PAS_ACTION_DM_APP_ARGS'), \
		 config_provider.get_config('PAS_ACTION_DM_APP_ENVS'),config_provider.get_config('PAS_ACTION_DM_APP_WDIR'), util.getValue("display"))
elif action == "GET_OTP":
    status = sessionmgr.gen_password()
elif action == "WAIT_ON_SESSION":
    sessionmgr.set_waitflag()
elif action == "STOP_SESSION":
    status = sessionmgr.stop_session()
elif action == "GET_SESSION":
    status = sessionmgr.get_session()
elif action == "SET_SESSION_EXPIRY":
    envs = config_provider.get_config("PAS_ACTION_DM_APP_ENVS")
    timeout = None
    if envs is not None:
        for entry in envs.split("\n"):
            splitwords = entry.split("=")
            var = splitwords[0]
            if var == 'SessionExpiry':
                timeout = splitwords[1]
                break
    status = sessionmgr.set_expiry(timeout)
else:
    sys.stderr.write("unsupported custom action type")

if not status:
    sys.stderr.write('execution error occurred')
    exit (1)

