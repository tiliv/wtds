import logging

from django.views.generic import View, ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import pluralize
from django.utils.translation import ungettext, ugettext as _

from extra_views import InlineFormSetView

from .models import Profile
from .forms import ProfileSwitchForm, ProfileForm

logger = logging.getLogger(__name__)

class AccountView(InlineFormSetView):
    model = User
    inline_model = Profile
    extra = 1
    template_name = "profiles/profiles.html"

    form_class = ProfileForm

    self_view = False
    section = "profiles"

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
        if not any((updated_count, deleted_count)):
            messages.info(self.request, _("No changes."))

        return response

    def formset_invalid(self, formset):
        response = super(AccountView, self).formset_invalid(formset)
        messages.error(self.request, _("Oops, something went wrong."))
        return response

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context.update({
            'total_uploads': self.request.user.wallpaper_set.count(),
            'uploads': self.request.user.wallpaper_set.filter_for_user(self.request.user),
        })
        return context

class UploadsView(ListView):
    template_name = "profiles/uploads.html"
    section = "uploads"

    def get_queryset(self):
        return self.request.user.wallpaper_set.filter_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UploadsView, self).get_context_data(**kwargs)
        context['total'] = self.request.user.wallpaper_set.count()
        return context

class FavoritesView(ListView):
    template_name = "profiles/favorites.html"
    section = "favorites"

    def get_queryset(self):
        return self.request.user.favorite_set.all().select_related('wallpaper')

    def get_context_data(self, **kwargs):
        context = super(FavoritesView, self).get_context_data(**kwargs)
        context['total'] = self.request.user.favorite_set.count()
        return context

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
        """ If none-value, deactivate.  Redirect as if it worked. """
        if not form['profile'].value():
            self.request.user.profile_set.deactivate()
        return super(ProfileSwitchView, self).form_valid(form)

class ProfileDeactivateView(View):
    def get(self, request):
        self.request.user.profile_set.deactivate()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', '/')
