import logging

from django.views.generic import View
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import pluralize
from django.utils.translation import ungettext, ugettext as _

from extra_views import InlineFormSetView

from .models import Profile
from .forms import ProfileSwitchForm

logger = logging.getLogger(__name__)

class AccountView(InlineFormSetView):
    model = User
    inline_model = Profile
    extra = 1

    self_view = False

    def get_object(self):
        if self.self_view: # no 'pk' or 'slug' in the url kwargs
            return self.request.user
        return super(AccountView, self).get_object()

    def formset_valid(self, formset):
        total_profiles = formset.initial_form_count()
        response = super(AccountView, self).formset_valid(formset)

        updated_count = len(formset.changed_objects)
        deleted_count = len(formset.deleted_objects)

        if updated_count:
            msg = ungettext(
                "Updated profile",
                "Updated %(count)d profiles",
                updated_count
            ) % {'count': updated_count}
            messages.success(self.request, msg)
        if deleted_count:
            msg = ungettext(
                "Deleted profile.",
                "Deleted %(count)d profiles.",
                deleted_count,
            ) % {'count': deleted_count}
            messages.success(self.request, msg)

        return response

    def formset_invalid(self, formset):
        response = super(AccountView, self).formset_invalid(formset)
        messages.error(self.request, _("Oops, something went wrong."))
        return response

class ProfileSwitchView(FormMixin, View):
    """ POST-only view for setting the profile via a ``ProfileSwitchForm`` submission. """

    form_class = ProfileSwitchForm # Form for listing the user's available profiles

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """ Adds ``user`` to form constructor arguments. """
        kwargs = super(ProfileSwitchView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    def form_valid(self, form):
        """ Make the profile active, redirect to where they came from. """
        form.cleaned_data['profile'].make_active()
        return super(ProfileSwitchView, self).form_valid(form)

    def form_invalid(self, form):
        """ Redirect the user back to where they came from. """
        return super(ProfileSwitchView, self).form_valid(form)
        