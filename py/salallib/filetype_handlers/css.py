from salallib.utilities import utilities

class ProcessCSS:
    
    #---------------------------------------------------------------------------

    name = '.css'
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_dir, target_dir, file_stem):
        utilities.substitute_variables(source_dir, target_dir, file_stem + '.css')
    
    #---------------------------------------------------------------------------

handler = ProcessCSS
