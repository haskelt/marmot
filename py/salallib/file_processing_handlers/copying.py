import os.path
import shutil
from salallib.log import log
from salallib.utilities import utilities

class Default:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['default']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        log.message('TRACE', 'Copying')
        shutil.copyfile(os.path.join(source_dir, file_stem + tag), os.path.join(target_dir, file_stem + tag))
    
    #---------------------------------------------------------------------------

handler = Default
