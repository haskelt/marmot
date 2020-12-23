from salallib.utilities import utilities

class ProcessCSS:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['.css']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        utilities.expand_template(source_dir, target_dir, file_stem + '.css')
    
    #---------------------------------------------------------------------------

handler = ProcessCSS
