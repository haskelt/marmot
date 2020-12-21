import os.path
import json
import argparse
from salal.log import log as log

# After initialization, the following attributes are available on
# the <config> object:
# - action: the action to be executed
# - profile: the build profile to use while executing it
# - system: a dict of system configuration variables
# - project: a dict of project configuration variables

class Config:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        cls.load_system_configuration ()
        cls.load_build_profiles ()
        cls.parse_arguments ()
        cls.initialize_variables ()
    
    #---------------------------------------------------------------------------

    @classmethod
    def load_system_configuration (cls):
        system_config_path = os.path.dirname(__file__) + '/system.json'
        log.message('debug', 'Loading system configuration from ' + system_config_path)
        with open(system_config_path) as system_variables_fh:
            cls.system = json.load(system_variables_fh) 

    #---------------------------------------------------------------------------

    @classmethod
    def load_build_profiles (cls):
        build_profiles_path = cls.system['config_root'] + cls.system['build_profiles_file']
        log.message('debug', 'Loading build profiles from ' + build_profiles_path)
        with open(build_profiles_path) as build_profiles_fh:
            cls._build_profiles = json.load(build_profiles_fh)
        
    #---------------------------------------------------------------------------

    @classmethod
    def parse_arguments (cls):
        log.message('debug', 'Parsing command-line arguments')
        parser = argparse.ArgumentParser()
        parser.add_argument('action', action = 'store')
        parser.add_argument('profile', action = 'store', nargs = '?', default = 'default')
        cls._arguments = parser.parse_args()
        cls.action = cls._arguments.action

    #---------------------------------------------------------------------------

    @classmethod
    def initialize_variables (cls):
        # convert the profile specifier to the correct profile name
        if cls._arguments.profile == 'default':
            cls.profile = None
            for build_profile in cls._build_profiles:
                if build_profile == 'common':
                    continue
                else:
                    cls.profile = build_profile
                    break
            if cls.profile == None:
                log.message('error', 'Default profile specified, but there are no profiles configured')
        elif cls._arguments.profile in cls._build_profiles:
            cls.profile = cls._arguments.profile
        else:
            log.message('error', 'Specified profile ' + cls._arguments.profile + ' does not exist')
        log.message('debug', 'Using profile ' + cls.profile)
            
        log.message('debug', 'Initializing system and project variables')
        cls.project = dict()
        profile_vars = { 'system': cls.system, 'project': cls.project }
        for var_type in ['system', 'project']:
            if 'common' in cls._build_profiles and var_type in cls._build_profiles['common']:
                profile_vars[var_type].update(cls._build_profiles['common'][var_type])
            if var_type in cls._build_profiles[cls.profile]:
                profile_vars[var_type].update(cls._build_profiles[cls.profile][var_type])
                
    #---------------------------------------------------------------------------

config = Config
