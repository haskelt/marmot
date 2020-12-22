import os
from salallib.log import log
from salallib.config import config

class Clean:

    #---------------------------------------------------------------------------
    
    name = 'clean'
    
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls):
        if 'clean_commands' not in config.system:
            log.message('error', 'No commands have been configured for the clean action')
        else:
            for command in config.system['clean_commands']:
                log.message('info', command)
                os.system(command)
 
    #---------------------------------------------------------------------------

handler = Clean
