import glob
import re
import os
import importlib
from salallib.config import config
from salallib.log import log

class Utilities:

    #---------------------------------------------------------------------------

    @classmethod
    def find_files (cls, directory, extension):
        # Recursively finds all files in the directory indicated by
        # <directory> that have the extension <extension>. Returns a list
        # of paths to these files relative to <directory>.
        result_list = []
        for absolute_path in glob.glob(directory + '**/*.' + extension, recursive = True):
            relative_path = re.match('^' + directory + '(.*)$', absolute_path).group(1)
            result_list.append(relative_path)
        return result_list

    #---------------------------------------------------------------------------

    @classmethod
    def load_handlers (cls, directory):
        handlers = dict()
        with os.scandir(os.path.join(config.system['salal_root'], directory)) as entries:
            for entry in entries:
                # filter files that start with a period or don't end
                # with .py
                if entry.is_file() and (not entry.name.startswith('.')) and entry.name.endswith('.py') and entry.name != '__init__.py':
                    package_specifier = os.path.normpath(os.path.join(directory, entry.name)).replace(os.sep, '.').replace('.py', '')
                    handler_module = importlib.import_module(package_specifier)
                    log.message('debug', handler_module.handler.name)
                    handlers[handler_module.handler.name] = handler_module.handler
        return handlers
    
    #---------------------------------------------------------------------------
    
utilities = Utilities
