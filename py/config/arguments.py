import argparse

class Arguments:

    #---------------------------------------------------------------------------

    def __init__ (self):
        parser = argparse.ArgumentParser()
        parser.add_argument('action', action = 'store')
        parser.add_argument('profile', action = 'store', nargs = '?', default = 'default')
        self.arguments = parser.parse_args()

    #---------------------------------------------------------------------------

    def __getitem__ (self, argument_name):
        return getattr(self.arguments, argument_name)

    #---------------------------------------------------------------------------

arguments = Arguments()
