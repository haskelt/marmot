import os
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities

class FileProcessing:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('DEBUG', 'Loading file processing handlers')
        cls.handlers = utilities.load_handlers(os.path.join(config.system['lib_root'], config.system['file_processing_handlers_dir']))

    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_dir, target_dir, file_relative_path):
        file_stem, ext = os.path.splitext(file_relative_path)
        if ext not in cls.handlers:
            log.message('ERROR', 'Handling for file type ' + ext + ' is not configured.')
        else:
            cls.handlers[ext].process(ext, source_dir, target_dir, file_stem)

    #---------------------------------------------------------------------------

file_processing = FileProcessing
