from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse

class AuthenticationMixin(object):
    login_required = True
    permissions_required = []

    def dispatch(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('auth:login'))
        if self.permissions_required:
            if not all(map(self.request.user.has_perm, self.permissions_required)):
                return HttpResponseForbidden()
        return super(AuthenticationMixin, self).dispatch(request, *args, **kwargs)
