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
        for file_relative_path in utilities.find_files(config.system['content_root'], 'xml'):
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(config.system['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('INFO', file_relative_path)
            file_processing.process(config.system['content_root'], config.system['profile_build_dir'], file_relative_path)

        # process JS and CSS files
        resources_path = os.path.join(config.system['design_root'], config.system['resources_dir'])
        js_files = utilities.find_files(resources_path, 'js')
        css_files = utilities.find_files(resources_path, 'css')
        for file_relative_path in js_files + css_files:
            # create the target directory if it doesn't exist
            os.makedirs(os.path.join(config.system['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
            log.message('INFO', file_relative_path)
            file_processing.process(resources_path, config.system['profile_build_dir'], file_relative_path)
            

    #---------------------------------------------------------------------------

handler = Build
