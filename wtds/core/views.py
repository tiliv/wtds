from functools import partial

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context

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

def _base_error(request, template_name=None):
    try:
        context = RequestContext(request)
        print context
    except Exception as e:
        context = Context()
    return render_to_response(template_name, context)

handler404 = partial(_base_error, template_name='404.html')
handler500 = partial(_base_error, template_name='500.html')
