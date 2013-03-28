from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string

# profile_switching_url = reverse_lazy('profile:switch')

from .forms import ProfileSwitchForm

def profile_switcher(request):
    if request.user.is_authenticated():
        return {'profile_switch_form': ProfileSwitchForm(request.user)}
    return {}
