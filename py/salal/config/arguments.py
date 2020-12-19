import argparse

#-------------------------------------------------------------------------------

def init ():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', action = 'store')
    parser.add_argument('profile', action = 'store', nargs = '?', default = 'default')
    arguments = parser.parse_args()
    return (arguments.action, arguments.profile)

#---------------------------------------------------------------------------

action, profile_specifier = init()
