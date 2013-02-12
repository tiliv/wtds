from django import forms
from django.contrib.auth.models import User

from .models import Profile

class ProfileSwitchForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=Profile.objects.none(), empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(ProfileSwitchForm, self).__init__(*args, **kwargs)

        profiles = user.profile_set.all()
        self.fields['profile'].queryset = profiles
        self.fields['profile'].initial = profiles.get_active()
