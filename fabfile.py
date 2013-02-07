import os.path

from fabric.api import env, run, cd, sudo, prefix
from fabric.tasks import Task

from tasks import manage
from tasks.utils import get_project_root

env.use_ssh_config = True
env.roledefs = {
    'staging': ['rydia'],
}

class Bounce(Task):
    name = "bounce"

    def run(self):
        sudo("service apache2 restart")

class Deploy(Task):
    name = "deploy"

    def run(self, syncdb=True, collectstatic=True):
        with cd(get_project_root()):
            with cd("wtds"):
                run("git pull")
                install_requirements.run()
                if syncdb:
                    manage.syncdb.run()
                manage.migrate.run()
                if collectstatic:
                    manage.collectstatic.run()
                bounce.run()

class InstallRequirements(Task):
    name = "install_requirements"
    
    def run(self, virtualenv="wtds"):
        with cd(get_project_root() + '/wtds'):
            with prefix('source /etc/bash_completion.d/virtualenvwrapper'):
                with prefix('workon {}'.format(virtualenv)):
                    run("pip install -r requirements.txt")

class Debug(Task):
    name = "debug"
    
    def run(self, command):
        with cd(get_project_root()):
            run(command)

bounce = Bounce()
deploy = Deploy()
install_requirements = InstallRequirements()
debug = Debug()
