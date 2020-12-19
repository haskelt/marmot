import salal.config as config
import salal.log as log
from . import build
from . import deploy

action_handlers = {
    'build': build.build,
    'deploy': deploy.deploy
}

#-------------------------------------------------------------------------------

def perform ():
    log.message('info', 'Beginning ' + config.action + ' for ' + config.profile + ' profile')
    action_handlers[config.action]()

#-------------------------------------------------------------------------------
