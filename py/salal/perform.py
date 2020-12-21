import salal.config as config
import salal.log as log
from . import handlers

#-------------------------------------------------------------------------------

def perform ():

    handler = handlers.get(config.action)
    if handler == None:
        log.message('error', 'Action ' + config.action + ' is not configured.')
    else:
        log.message('info', 'Beginning ' + config.action + ' for ' + config.profile + ' profile')
        handler()

#-------------------------------------------------------------------------------
