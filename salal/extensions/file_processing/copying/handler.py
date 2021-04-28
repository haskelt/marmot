# This handler just copies the file from the source directory to the target
# directory.
import os.path
import shutil
from salal.core.logging import logging

class Default:

    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['default']
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_target_extension(cls, source_ext):
        return source_ext
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_file_path, target_file_path):
        logging.message('TRACE', 'Copying')
        shutil.copyfile(source_file_path, target_file_path)
    
    #---------------------------------------------------------------------------

handler = Default
