from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
)
from allauth.account.forms import SignupForm as BaseSignupForm

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
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user