import json
from .constants import constants

class Profiles:

    #---------------------------------------------------------------------------

    def __init__ (self):
        # load the build profiles
        with open(constants['config_root'] + constants['build_profiles_file']) as build_profiles_fh:
            build_profiles = json.load(build_profiles_fh)
        
    #---------------------------------------------------------------------------

    def __getitem__ (self, profile_name):
        return self.build_profiles[profile_name]

    #---------------------------------------------------------------------------

    def variables (self, profile_name):
        variables = dict()
        if 'common' in self.build_profiles:
            variables.update(self.build_profiles['common']['variables'])
        variables.update(build_profiles[profile_name]['variables'])
        return variables
    
#---------------------------------------------------------------------------

profiles = Profiles()
