import glob
import os
import re
from salal.log import log as log
from salal.config import config as config
from . import render

class Build:
    
    #---------------------------------------------------------------------------

    name = 'build'
    
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls):
        log.message('info', 'building')
        for xml_file in glob.glob(config.system['content_root'] + '**/*.xml', recursive = True):
            # this is the part of the path to the XML file that will get recreated
            # in the build directory
            file_stem = re.match('^' + config.system['content_root'] + '(.*)\.xml$', xml_file).group(1)
            # create the target directory if it doesn't exist
            os.makedirs(config.system['build_root'] + config.profile + '/' + os.path.dirname(file_stem), exist_ok = True)
            print(file_stem)
            render.render_page(file_stem)

    #---------------------------------------------------------------------------

handler = Build
