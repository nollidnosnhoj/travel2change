from django import forms
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import (
    authenticate, get_user_model
)

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'authform'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            PrependedText(
                'email', 
                '<i class="fa fa-envelope"></i>', 
                placeholder='Email Address'
            ),
            PrependedText(
                'password',
                '<i class="fa fa-key"></i>', 
                placeholder='Password',
            ),
            Submit('submit', 'Login', css_class='btn-success btn-lg btn-block')
        )
    
    email       = forms.EmailField()
    password    = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'authform'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            PrependedText(
                'email', 
                '<i class="fa fa-envelope"></i>', 
                placeholder='Email Address'
            ),
            PrependedText(
                'first_name',
                '<i class="fa fa-user"></i>', 
                placeholder='First Name'
            ),
            PrependedText(
                'last_name',
                '<i class="fa fa-user"></i>', 
                placeholder='Last Name'
            ),
            PrependedText(
                'password',
                '<i class="fa fa-key"></i>', 
                placeholder='Password',
            ),
            Submit('submit', 'Register', css_class='btn-success btn-lg btn-block')
        )
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
