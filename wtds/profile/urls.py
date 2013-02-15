from django.conf.urls import patterns, include, url

from .views import AccountView, ProfileSwitchView, ProfileDeactivateView

urlpatterns = patterns('',
    url(r'^$', AccountView.as_view(self_view=True), name='view'),
    url(r'^switch/$', ProfileSwitchView.as_view(), name='switch'),
    url(r'^off/$', ProfileDeactivateView.as_view(), name='deactivate'),
)
