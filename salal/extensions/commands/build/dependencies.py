from salal.core.log import log

class DependencyManager:
    
    #---------------------------------------------------------------------------

    @classmethod
    def read_log (cls):
        log.message('TRACE', 'Reading dependency log')
    
    #---------------------------------------------------------------------------

    @classmethod
    def needs_build (cls, target_file, source_file):
        return True

    #---------------------------------------------------------------------------

    @classmethod
    def queue_log_update (cls, target_file, source_file):
        pass
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def write_log (cls):
        log.message('TRACE', 'Writing dependency log')

    #---------------------------------------------------------------------------
    
dependencies = DependencyManager
