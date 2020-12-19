import os
import salal.log as log
import salal.config as config

#-------------------------------------------------------------------------------

def deploy ():
    if 'deploy_command' not in config.system:
        log.message('error', 'No deploy command configured in current profile')
    if 'deploy_destination' not in config.system:
        log.message('error', 'No deploy destination configured in current profile')
    
    deploy_string = config.system['deploy_command'].replace('{{build_dir}}', config.build_root + config.profile).replace('{{deploy_destination}}', config.system['deploy_destination'])
    log.message('info', deploy_string)
    os.system(deploy_string)
 
#-------------------------------------------------------------------------------
