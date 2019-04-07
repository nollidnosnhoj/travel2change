from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.utils.translation import ugettext as _
from allauth.account.forms import SignupForm as BaseSignupForm
from allauth.account.models import EmailAddress
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


class HostUpdateForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ('_name', 'custom_slug', 'description', 'phone', 'website')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['contact_email'] = forms.ModelChoiceField(
            queryset=EmailAddress.objects.filter(user=self.user).all(),
            required=False,
        )


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
        user = super().save(request)
        is_host = self.cleaned_data['is_host']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if is_host:
            host = Host.objects.create(user=user)
            host.save()
        return user
