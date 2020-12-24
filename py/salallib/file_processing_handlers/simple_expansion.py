from salallib.log import log
from salallib.utilities import utilities

class SimpleExpansion:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['.js', '.css']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        log.message('TRACE', 'Doing simple expansion')
        utilities.expand_template(source_dir, target_dir, file_stem + tag)
    
    #---------------------------------------------------------------------------

handler = SimpleExpansion
