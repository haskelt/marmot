import glob
import os
import os.path
import re
import salal.config as config
from . import render

#-------------------------------------------------------------------------------

def build ():
    for xml_file in glob.glob(config.content_root + '**/*.xml', recursive = True):
        # this is the part of the path to the XML file that will get recreated
        # in the build directory
        file_stem = re.match('^' + config.content_root + '(.*)\.xml$', xml_file).group(1)
        # create the target directory if it doesn't exist
        os.makedirs(config.build_root + config.profile + '/' + os.path.dirname(file_stem), exist_ok = True)
        print(file_stem)
        render.render_page(file_stem)

#-------------------------------------------------------------------------------
