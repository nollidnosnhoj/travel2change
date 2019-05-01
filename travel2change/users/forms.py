from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.utils.translation import ugettext as _
from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm as BaseSignupForm
from users.models import Host

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class SignupForm(BaseSignupForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name  = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    is_host = forms.BooleanField(
        required=False,
        label=_('Create a Host Profile?')
    )

    @transaction.atomic
    def save(self, request):
        """
        If the 'Create Host Profile' checked, it will create a host profile object.
        It is important that transaction is atomic, since we are saving multiple
            different objects at once.
        """
        user = super().save(request)
        is_host = self.cleaned_data['is_host']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if is_host:
            host = Host.objects.create(user=user)
            host.save()
        return user

# Overriding Django Allauth LoginForm to compat with Django Axes
# https://django-axes.readthedocs.io/en/latest/usage.html#integration-with-django-allauth
class LoginForm(LoginForm):
    def user_credentials(self):
        credentials = super().user_credentials()
        credentials['login'] = credentials.get('email') or credentials.get('username')
        return credentials
