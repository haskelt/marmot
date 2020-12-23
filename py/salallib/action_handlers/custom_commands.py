import os
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities

class CustomCommands:

    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        # This determines what custom commands we have based on the
        # <action_commands> system variable.
        if 'action_commands' in config.system:
            return config.system['action_commands'].keys()
        else:
            return []
    
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, tag):
        # Iterates through the list of commands associated with 'tag',
        # does substitution for system variables, and passes them to
        # the OS for execution
        for command_template in config.system['action_commands'][tag]:
            command_string = utilities.substitute_variables(command_template, config.system)
            log.message('INFO', command_string)
            os.system(command_string)
 
    #---------------------------------------------------------------------------

handler = CustomCommands
