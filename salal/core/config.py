import sys
import os.path
import json
import argparse
from salal.core.logging import logging
from salal.core.utilities import utilities

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
        cls.set_salal_root()
        cls.parse_arguments()
        cls.load_system_configuration()
        cls.load_user_configuration()
        cls.load_project_configuration()
        cls.initialize_variables()
        cls.set_extension_directories()
        
    #---------------------------------------------------------------------------
 
    @classmethod
    def set_salal_root (cls):
        cls.parameters = {}
        cls.parameters['paths'] = {}
        cls.parameters['paths']['salal_root'] = os.path.normpath(os.path.dirname(sys.modules['__main__'].__file__))
    
    #---------------------------------------------------------------------------
   
    @classmethod
    def parse_arguments (cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('action', action = 'store')
        parser.add_argument('profile', action = 'store', nargs = '?', default = 'default')
        parser.add_argument('--config-file', action = 'store', default = os.path.join(cls.parameters['paths']['salal_root'], 'system_config.json'))
        parser.add_argument('--logging-level', action = 'store', default = 'INFO')
        cls._arguments = parser.parse_args()
        # we shouldn't do any logging until this point has been reached,
        # otherwise it won't be impacted by the logging level
        logging.set_logging_level(cls._arguments.logging_level)
        cls.action = cls._arguments.action
        logging.message('DEBUG', 'Parsed command line arguments')

    #---------------------------------------------------------------------------

    @classmethod
    def load_system_configuration (cls):
        logging.message('DEBUG', 'Loading system configuration from ' + cls._arguments.config_file)
        with open(cls._arguments.config_file) as system_config_fh:
            utilities.deep_update(cls.parameters, json.load(system_config_fh))

    #---------------------------------------------------------------------------

    @classmethod
    def load_user_configuration (cls):
        config_file = os.path.expanduser(cls.parameters['paths']['user_config_file'])
        if os.path.isfile(config_file):
            logging.message('DEBUG', 'Loading user configuration from ' + config_file)
            with open(config_file) as user_config_fh:
                utilities.deep_update(cls.parameters, json.load(user_config_fh))

    #---------------------------------------------------------------------------

    @classmethod
    def load_project_configuration (cls):
        logging.message('DEBUG', 'Loading project configuration from ' + cls.parameters['paths']['project_config_file'])
        with open(cls.parameters['paths']['project_config_file']) as project_config_fh:
            cls._project_config = json.load(project_config_fh)
        
    #---------------------------------------------------------------------------

    @classmethod
    def initialize_variables (cls):
        logging.message('DEBUG', 'Using salal root directory of ' + cls.parameters['paths']['salal_root'])
        # convert the profile specifier to the correct profile name
        if cls._arguments.profile == 'default':
            cls.parameters['profile'] = None
            for build_profile in cls._project_config:
                if build_profile == 'common':
                    continue
                else:
                    cls.parameters['profile'] = build_profile
                    break
            if cls.parameters['profile'] == None:
                logging.message('ERROR', 'Default profile specified, but there are no profiles configured')
        elif cls._arguments.profile in cls._project_config:
            cls.parameters['profile'] = cls._arguments.profile
        else:
            logging.message('ERROR', 'Specified profile ' + cls._arguments.profile + ' does not exist')
        logging.message('INFO', 'Using profile ' + cls.parameters['profile'])
        cls.parameters['paths']['profile_build_dir'] = os.path.join(cls.parameters['paths']['build_root'], cls.parameters['profile'])
        
        logging.message('DEBUG', 'Initializing system and project variables')
        cls.site = dict()
        profile_vars = { 'parameters': cls.parameters, 'site': cls.site }
        for var_type in ['parameters', 'site']:
            if 'common' in cls._project_config and var_type in cls._project_config['common']:
                utilities.deep_update(profile_vars[var_type], cls._project_config['common'][var_type])
            if var_type in cls._project_config[cls.parameters['profile']]:
                utilities.deep_update(profile_vars[var_type], cls._project_config[cls.parameters['profile']][var_type])
        if 'theme_root' in config.parameters['paths']:
            logging.message('INFO', 'Using theme ' + config.parameters['paths']['theme_root'])
                
    #---------------------------------------------------------------------------

    @classmethod
    def set_extension_directories (cls):
        # Extensions can be located in three places: The base Salal
        # directory, the theme directory, or the <design> directory
        # for the project. In each case, any extensions need to be
        # placed in an <extensions> directory in that location. Here
        # we check for the existence of these <extensions> directories,
        # and set the system path <extension_dirs> to a list of those that
        # are found.
        extension_locations = [
            cls.parameters['paths']['salal_root'],
            cls.parameters['paths']['theme_root'] if 'theme_root' in config.parameters['paths'] else None,
            'design'
        ]
        config.parameters['paths']['extension_dirs'] = []
        for location in extension_locations:
            if location:
                extension_dir = os.path.join(location, cls.parameters['paths']['extensions_root'])
                if os.path.isdir(extension_dir):
                    config.parameters['paths']['extension_dirs'].append(extension_dir)
                    logging.message('DEBUG', 'Registered extensions directory ' + extension_dir)
        
    #---------------------------------------------------------------------------
    
config = Config
