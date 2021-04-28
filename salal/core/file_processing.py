import os
from salal.core.logging import logging
from salal.core.config import config
from salal.core.handlers import handlers
from salal.core.dependencies import dependencies

class FileProcessing:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        logging.message('DEBUG', 'Loading file processing handlers')
        cls.handlers = handlers.load_handlers(config.system['paths']['file_processing_handlers_dir'])
        
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_file_path, target_file_path):
        file_stem, ext = os.path.splitext(source_file_path)
        if file_stem.startswith('.'):
            ext = file_stem
            file_stem = ''
        # strip off the initial '.' in the extension so we just have letters
        ext = ext[1:]
        if ext in cls.handlers:
            tag = ext
        elif 'default' in cls.handlers:
            tag = 'default'
        else:
            logging.message('WARN', 'Handling for file type ' + ext + ' is not configured, skipping.')
            return
        if dependencies.needs_build(target_file_path, source_file_path):
            # create the target directory if it doesn't exist
            os.makedirs(os.path.dirname(target_file_path), exist_ok = True)
            logging.message('INFO', target_file_path)
            dependencies.start_build_tracking(target_file_path, source_file_path)
            cls.handlers[tag].process(source_file_path, target_file_path)
            dependencies.stop_build_tracking()
        else:
            logging.message('TRACE', target_file_path + ' is up to date, skipping')

    #---------------------------------------------------------------------------

file_processing = FileProcessing
