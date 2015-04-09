from TurboVNCSessionManager import TurboVNCSessionManager

# Provides different Session Manager instances

class SessionManagerProvider:

    def __init__(self):
        self.vnc_sessionmgr = TurboVNCSessionManager()

    def get_session_mgr(self, sol_type):
        if sol_type == "TurboVNC":
            return self.vnc_sessionmgr
        else:
             return None
