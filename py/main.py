import glob
# local packages
import config
import render

def build ():
    xml_files = glob.glob(config.constants['content_root'] + '**/*.xml', recursive = True)
    for file in xml_files:
        print(file)
        render.render_page('index')


build()
