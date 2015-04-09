import os

# An implementation that looks up the environment 

class ConfigurationProvider:

    def get_config(self, name):
        return os.getenv(name)
