import os
from salallib.log import log
from salallib.config import config

class Deploy:

    #---------------------------------------------------------------------------

    name = 'deploy'
    
    #---------------------------------------------------------------------------

    def execute ():
        if 'deploy_command' not in config.system:
            log.message('error',
                        'No deploy command configured in current profile')
        if 'deploy_destination' not in config.system:
            log.message('error',
                        'No deploy destination configured in current profile')
        for command in config.system['deploy_commands']:
            execution_string = command.replace('{{build_dir}}', config.system['build_root'] + config.profile).replace('{{deploy_destination}}', config.system['deploy_destination'])
            log.message('info', execution_string)
            os.system(execution_string)
 
    #---------------------------------------------------------------------------

handler = Deploy
