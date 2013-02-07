from fabric.tasks import Task
from fabric.api import env, run, cd, sudo, prefix

from .utils import get_project_root, get_settings_module

class Manage(Task):
    name = "manage"

    def run(self, command, settings=None, virtualenv='wtds'):
        if settings is None:
            settings = get_settings_module()
        command = "./manage.py {} --settings={}".format(command, settings)
        with cd(get_project_root() + '/wtds'):
            with prefix('source /etc/bash_completion.d/virtualenvwrapper'):
                with prefix('workon {}'.format(virtualenv)):
                    run(command)

class ManagementCommandTaskBase(object):
    """ Mixin for tasks that want to run a ``manage.py`` command. """
    name = None

    def run(self, settings=None, virtualenv=None):
        manage.run(self.name, settings)

class SyncDB(ManagementCommandTaskBase, Task):
    name = "syncdb"

class CollectStatic(ManagementCommandTaskBase, Task):
    name = "collectstatic"

class Migrate(ManagementCommandTaskBase, Task):
    name = "migrate"

    def run(self, apps=None, fake=None, **kwargs):
        command = self.name
        if apps:
            command += " " + apps
        if fake:
            command += " --fake " + fake
        manage.run(command, **kwargs)

class SchemaMigration(ManagementCommandTaskBase, Task):
    name = "schemamigration"

    def run(self, apps=None, fake=None, **kwargs):
        command = self.name
        if apps:
            command += " " + apps
        if fake:
            command += " --fake " + fake
        manage.run(command, **kwargs)

manage = Manage(default=True)
syncdb = SyncDB()
migrate = Migrate()
collectstatic = CollectStatic()
