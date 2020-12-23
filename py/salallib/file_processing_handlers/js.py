from salallib.utilities import utilities

class ProcessJS:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['.js']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, tag, source_dir, target_dir, file_stem):
        utilities.expand_template(source_dir, target_dir, file_stem + '.js')
    
    #---------------------------------------------------------------------------

handler = ProcessJS
