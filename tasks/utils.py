from fabric.api import run, env, cd

SERVER_PROJECT_ROOTS = {
    'rydia': '/home/tim/sites/wallpapersthatdontsuck.com',
}

def determine_current_role():
    """ See https://github.com/fabric/fabric/pull/824. """
    for role, hosts in env.roledefs.items():
        if env.host_string in hosts:
            return role

def get_project_root():
    return SERVER_PROJECT_ROOTS[env.host_string]

def get_settings_module():
    return 'wtds.settings.{}'.format(determine_current_role())
