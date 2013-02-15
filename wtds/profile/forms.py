from django import forms
from django.contrib.auth.models import User

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'optional'}),
            'ratio_style': forms.Select(attrs={'tabindex': -1}),
            'width_style': forms.Select(attrs={'tabindex': -1}),
            'height_style': forms.Select(attrs={'tabindex': -1}),
        }
    

class ProfileSwitchForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=Profile.objects.none(), empty_label=unicode(Profile()))

    def __init__(self, user, *args, **kwargs):
        super(ProfileSwitchForm, self).__init__(*args, **kwargs)

        profiles = user.profile_set.all()
        self.fields['profile'].queryset = profiles
        self.fields['profile'].initial = profiles.get_active()
