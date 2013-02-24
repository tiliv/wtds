from django.conf.urls import patterns, include, url

from .views import (AccountView, UploadsView, FavoriteListView, FavoriteCreateView,
        FavoriteDeleteView, ProfileSwitchView, ProfileDeactivateView)

urlpatterns = patterns('',
    url(r'^$', AccountView.as_view(self_view=True), name='view'),
    url(r'^uploads/$', UploadsView.as_view(), name='uploads'),
    url(r'^favorites/', include(patterns('',
        url(r'^$', FavoriteListView.as_view(), name='list'),
        url(r'^(?P<pk>\d+)/add/$', FavoriteCreateView.as_view(), name='add'),
        url(r'^(?P<pk>\d+)/remove/$', FavoriteDeleteView.as_view(), name='remove'),
    ), namespace="favorites")),
    url(r'^switch/$', ProfileSwitchView.as_view(), name='switch'),
    url(r'^off/$', ProfileDeactivateView.as_view(), name='deactivate'),
)
