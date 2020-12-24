import os
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities 
from salallib.file_processing import file_processing

class Build:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['build']
    
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, tag):
        # build HTML pages
        for file_relative_path in utilities.find_files_by_extension(config.system['content_root'], 'xml'):
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(config.system['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('INFO', file_relative_path)
            file_processing.process(config.system['content_root'], config.system['profile_build_dir'], file_relative_path)

        # Process theme (if set) and local resource files. Theme files get
        # processed first, so they can be overridden by local files. This
        # is accomplished simply by overwriting the theme version of the
        # file.
        resource_dirs = [os.path.join(config.system['design_root'], config.system['resource_dir'])]
        if('theme_root' in config.system):
            resource_dirs.insert(0, os.path.join(config.system['theme_root'], config.system['resource_dir']))
        for resource_dir in resource_dirs:
            log.message('DEBUG', 'Processing resources from ' + resource_dir)
            resource_files = utilities.find_files(resource_dir)
            for file_relative_path in resource_files:
                # create the target directory if it doesn't exist
                os.makedirs(os.path.join(config.system['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
                log.message('INFO', file_relative_path)
                file_processing.process(resource_dir, config.system['profile_build_dir'], file_relative_path)
            

    #---------------------------------------------------------------------------

handler = Build
