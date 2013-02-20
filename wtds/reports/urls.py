"""
URLs for including from other apps.  When included, declare an instance namespace.

"""

from django.conf.urls import patterns, include, url

from .views import ReportListView, ReportCreateView

urlpatterns = patterns('',
    # List views
    url(r'^$', ReportListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/', include(patterns('',
        url(r'^$', ReportListView.as_view(), name="list"),
        url(r'^new/$', ReportCreateView.as_view(), name="create"),
        url(r'^(?P<field_name>[a-z_][a-zA-Z\d_]*)/', include(patterns('',
            url(r'$', ReportListView.as_view(), name="list"),
            url(r'^new/$', ReportCreateView.as_view(), name="create"),
        )))
    ))),
)
