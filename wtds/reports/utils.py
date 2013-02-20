from django.conf.urls import include

from . import urls

def include_reports_urls(app_name, url='reports'):
    """
    Shorthand method for returning a urlconf inclusion of the reports urls with an instance
    namespace of ``app_name``.

    The ``app_name`` is required, to provide the necessary hints to the views that will display
    results scoped by content type.

    The default url for the regex is ``"reports"``, but can be overriden by specifying the ``url``
    parameter with a string component name such as ``"issues"``, without the trailing slash.  If
    necessary, the url component can be removed entirely (mounting the report urls directly into the
    calling structure) by sending a blank or ``None`` value.

    """

    if url:
        url += "/"
    return (r'^%s' % url, include(urls, namespace="reports", app_name=app_name))
