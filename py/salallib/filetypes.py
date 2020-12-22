import os
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities

class FileTypes:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('debug', 'Loading file type handlers')
        cls.handlers = utilities.load_handlers(os.path.join(config.system['lib_root'], config.system['filetype_handlers_dir']))

    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_dir, target_dir, file_relative_path):
        file_stem, ext = os.path.splitext(file_relative_path)
        if ext not in cls.handlers:
            log.message('error', 'Handling for file type ' + ext + ' is not configured.')
        else:
            cls.handlers[ext].process(source_dir, target_dir, file_stem)

    #---------------------------------------------------------------------------

filetypes = FileTypes
