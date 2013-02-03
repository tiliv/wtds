# wtds

Django codebase for Wallpapers That Don't Suck website

## Setup

WTDS uses multiple settings modules in the `settings/` directory.  Specify the one you want to use when using the `manage.py` or `django-admin.py` scripts via the `--settings` command line option.

`settings/base.py` is a fully valid settings module, but depends on the following environment variables:

* `WTDS_DATABASE_USER`
* `WTDS_DATABASE_PASSWORD`
* `WTDS_DATABASE_SECRET_KEY`

These settings are potentially sensitive and should not be committed to the repository.  For most development needs, these variables can simply be exported in `.bash_profile`.  For production, variables such as these could be made available in the system's `/etc/launchd.conf` or similar.

Create a settings module in `wtds/settings/` and import from the `base` or `development` modules to avoid changing settings for other developers.

## TextMate helpers

* [django-tools.tmbundle](https://github.com/tiliv/django-tools.tmbundle): general Django/pip/virtualenv bundle with lots of shortcuts for running management commands in Terminal
* [django-templates.tmbundle](https://github.com/tiliv/textmate-django-templates): a thorough Django template HTML grammar.  The one in the TextMate repository list is really quite crumby.
