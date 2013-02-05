import os.path

from fabric.api import env, run, cd, sudo
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

    def run(self):
        with cd(get_project_root()):
            with cd("wtds"):
                run("git pull")
                bounce.run()

class Debug(Task):
    name = "debug"
    
    def run(self, command):
        with cd(get_project_root()):
            run(command)

bounce = Bounce()
deploy = Deploy()
debug = Debug()
