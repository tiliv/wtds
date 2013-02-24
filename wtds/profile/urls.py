from django.conf.urls import patterns, include, url

from .views import AccountView, UploadsView, FavoritesView, ProfileSwitchView, ProfileDeactivateView

urlpatterns = patterns('',
    url(r'^$', AccountView.as_view(self_view=True), name='view'),
    url(r'^uploads/$', UploadsView.as_view(), name='uploads'),
    url(r'^favorites/$', FavoritesView.as_view(), name='favorites'),
    url(r'^switch/$', ProfileSwitchView.as_view(), name='switch'),
    url(r'^off/$', ProfileDeactivateView.as_view(), name='deactivate'),
)
