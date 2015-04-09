#coding: utf-8

sys.path.append(scriptDir)
import RefreshUtils
import Utils

Debug = True

if (Debug is True):
    refresh_utils = RefreshUtils.RefreshUtils(applicationArgs, refreshSourceName, Debug)

utils = Utils.Utils()
