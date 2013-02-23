from django.db import DEFAULT_DB_ALIAS, router
from django.db.models import signals

from .. import models
from ..constants import STANDARD_USER_GROUP_NAME, STANDARD_USER_GROUP_PERMISSIONS

def create_groups(app, created_models, verbosity, db=DEFAULT_DB_ALIAS, **kwargs):
    from django.contrib.auth.models import Group, Permission
    group, created = Group.objects.using(db).get_or_create(name=STANDARD_USER_GROUP_NAME)

    if created and verbosity >= 2:
        print("Adding core group '%s'" % STANDARD_USER_GROUP_NAME)

    permissions = Permission.objects.using(db).filter(codename__in=STANDARD_USER_GROUP_PERMISSIONS)
    group.permissions.add(*permissions)

    if verbosity >= 2:
        for perm in STANDARD_USER_GROUP_PERMISSIONS:
            print("Adding core permission '%s' to group '%s'" % (perm, STANDARD_USER_GROUP_NAME))

signals.post_syncdb.connect(create_groups, sender=models)
