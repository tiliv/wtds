from django.conf.urls import patterns, include, url

from .views import ReportListView, ReportCreateView, ReportDetailView

urlpatterns = patterns('',
    url(r'^$', ReportListView.as_view(), name="reports"),
    url(r'^create/$', ReportCreateView.as_view(), name="create"),
    url(r'^(?P<contenttype>[\w_]+)/', include(patterns('',
        url(r'^$', ReportListView.as_view(), name="reports"),
        url(r'^create/$', ReportCreateView.as_view(), name="create"),
        url(r'^(?P<model_pk>[^/]+)/', include(patterns('',
            url(r'^$', ReportListView.as_view(), name="reports"),
            url(r'^create/$', ReportCreateView.as_view(), name="create"),
            url(r'^(?P<field_name>[a-zA-Z_]+)/', include(patterns('',
                url(r'^$', ReportListView.as_view(), name="reports"),
                url(r'^create/$', ReportCreateView.as_view(), name="create"),
                url(r'^(?P<pk>\d+)/$', ReportDetailView.as_view(), name="report"),
            ))),
        ))),
    ))),
)
