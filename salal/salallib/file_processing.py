import os
from salal.salallib.log import log
from salal.salallib.config import config
from salal.salallib.utilities import utilities

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
        # strip off the initial '.' in the extension so we just have letters
        ext = ext[1:]
        if ext in cls.handlers:
            tag = ext
        elif 'default' in cls.handlers:
            tag = 'default'
        else:
            log.message('WARN', 'Handling for file type ' + ext + ' is not configured, skipping.')
            return
        cls.handlers[tag].process(ext, source_dir, target_dir, file_stem)

    #---------------------------------------------------------------------------

file_processing = FileProcessing
