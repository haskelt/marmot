import os
from salallib.log import log
from salallib.config import config
from salallib.utilities import utilities 
from salallib.filetypes import filetypes

class Build:
    
    #---------------------------------------------------------------------------

    name = 'build'
    
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls):
        # build HTML pages
        for file_relative_path in utilities.find_files(config.system['content_root'], 'xml'):
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(config.system['profile_build_root'], os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('info', file_relative_path)
            filetypes.process(config.system['content_root'], config.system['profile_build_root'], file_relative_path)

        # process JS and CSS files
        resources_path = os.path.join(config.system['design_root'], config.system['resources_dir'])
        js_files = utilities.find_files(resources_path, 'js')
        css_files = utilities.find_files(resources_path, 'css')
        for file_relative_path in js_files + css_files:
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(config.system['profile_build_root'], os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('info', file_relative_path)
            filetypes.process(resources_path, config.system['profile_build_root'], file_relative_path)
            

    #---------------------------------------------------------------------------

handler = Build
