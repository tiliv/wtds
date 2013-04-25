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

def _base_error(request, status_code, template_name=None, fake=False):
    context = {'fake': fake}
    try:
        context = RequestContext(request, context)
    except Exception as e:
        context = Context(context)
    response = render_to_response(template_name, context)
    response.status_code = status_code
    return response

handler403 = partial(_base_error, status_code=403, template_name='403.html')
handler404 = partial(_base_error, status_code=404, template_name='404.html')
handler500 = partial(_base_error, status_code=500, template_name='500.html')
