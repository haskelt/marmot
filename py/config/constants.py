
class Constants:

    #---------------------------------------------------------------------------

    def __init__ (self):
        self.constants = {
            "config_root": "config/",
            "content_root": "content/",
            "build_root": "build/",
            "build_profiles_file": "profiles.json"
        }

    #---------------------------------------------------------------------------

    def __getitem__ (self, item):
        return self.constants[item]

    #---------------------------------------------------------------------------


constants = Constants()
