import json
import salal.log as log
from . import constants
from . import arguments

#-------------------------------------------------------------------------------

def init ():
    # load the build profiles
    with open(constants.config_root + constants.build_profiles_file) as build_profiles_fh:
        build_profiles = json.load(build_profiles_fh)

    # convert the profile specifier to the correct profile name
    if arguments.profile_specifier == 'default':
        profile = None
        for build_profile in build_profiles:
            if build_profile == 'common':
                continue
            else:
                profile = build_profile
                break
        if profile == None:
            log.message('error', 'Default profile specified, but there are no profiles configured')
    elif arguments.profile_specifier in build_profiles:
        profile = arguments.profile_specifier
    else:
        log.message('error', 'Specified profile does not exist')

    # initialize system and project variables
    profile_vars = dict()
    for var_type in ['system', 'project']:
        profile_vars[var_type] = dict()
        if 'common' in build_profiles and var_type in build_profiles['common']:
            profile_vars[var_type].update(build_profiles['common'][var_type])
        if var_type in build_profiles[profile]:
            profile_vars[var_type].update(build_profiles[profile][var_type])
    return (profile, profile_vars['system'], profile_vars['project'])
                
#-------------------------------------------------------------------------------

profile, system, project = init()
