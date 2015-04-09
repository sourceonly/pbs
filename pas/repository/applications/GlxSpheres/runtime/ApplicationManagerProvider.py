from VGLApplicationManager import VGLApplicationManager

# Provides different Application Manager instances
class ApplicationManagerProvider:

    def __init__(self):
        self.vgl_app_mgr = VGLApplicationManager()

    def get_app_mgr(self, sol_type):
        if sol_type == "VGL":
            return self.vgl_app_mgr
        else:
             return None
