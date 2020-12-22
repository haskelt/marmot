import os
import importlib
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities

class Actions:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('debug', 'Loading action handlers')
        cls.handlers = utilities.load_handlers(os.path.join(config.system['lib_root'], config.system['action_handlers_dir']))
        
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, action):
        if action not in cls.handlers:
            log.message('error', 'Action ' + action + ' is not configured.')
        else:
            log.message('info', 'Beginning ' + action + ' for ' + config.profile + ' profile')
            cls.handlers[action].execute()

    #---------------------------------------------------------------------------

actions = Actions
