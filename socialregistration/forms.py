from django import forms
from django.utils.translation import gettext as _

from django.contrib.auth.models import User

class ExistingUser(Exception):
    def __init__(self):
        """This user already exists, display the claim form instead."""

class UserForm(forms.Form):
    username = forms.RegexField(r'^\w+$', max_length=32)
    email = forms.EmailField(required=False)

    def __init__(self, user, profile, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = profile

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise ExistingUser()

    def save(self):
        self.user.username = self.cleaned_data.get('username')
        self.user.email = self.cleaned_data.get('email')
        self.user.save()
        self.profile.user = self.user
        self.profile.save()
        return self.user

class ClaimForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    submitted = forms.CharField(initial='true', widget=forms.HiddenInput)

    def __init__(self, user, profile, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = profile

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            self.user = user
            return username
        except User.DoesNotExist:
            raise forms.ValidationError(_("The username you supplied is not in use."))

    def clean(self):
        account = User.objects.get(username=self.cleaned_data.get('username'))
        if account.check_password(self.cleaned_data.get('password')):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("The password you entered was incorrect."))

    def save(self):
        self.profile.user = self.user
        self.profile.save()
        return self.user
