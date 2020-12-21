import os
import importlib
from salal.log import log as log
from salal.config import config as config

class Actions:

    #---------------------------------------------------------------------------
    
    action_handlers = dict()

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        basepath = os.path.dirname(__file__) + '/action_handlers'
        with os.scandir(basepath) as entries:
            for entry in entries:
                if entry.is_dir() and entry.name != '__pycache__':
                    handler_module = importlib.import_module('salal.action_handlers.' + entry.name)
                    log.message('debug', 'Loaded handler for action ' + handler_module.handler.name)
                    cls.action_handlers[handler_module.handler.name] = handler_module.handler

    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, action):
        if action not in cls.action_handlers:
            log.message('error', 'Action ' + action + ' is not configured.')
        else:
            log.message('info', 'Beginning ' + action + ' for ' + config.profile + ' profile')
            cls.action_handlers[action].execute()

    #---------------------------------------------------------------------------

actions = Actions
