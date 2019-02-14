from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from django.contrib.auth import (
    authenticate, get_user_model
)
from django.contrib.auth.password_validation import (
    password_validators_help_texts, validate_password
)
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row, Column, HTML
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

    email       = forms.EmailField()
    password    = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    # Form Builder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = False
        self.fields['password'].label = False
        self.helper = FormHelper()
        self.helper.form_class = 'authform'
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
            Row(
                Column(
                    'remember_me',
                    css_class="col-md-6 col-xs-6 mb-0",
                ),
                Column(
                    HTML("<a class='form-group forgot-pass' href='#'>Forgot Password</a>"),
                    css_class="col-md-6 col-xs-6 mb-0",
                ),
                css_class="form-row",
            ),
            Submit('submit', 'Login', css_class='btn-success btn-lg btn-block')
        )

    # Authentication Validation
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError(_("Email or Password is Incorrect."))

class RegisterForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    # Form Builder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'authform'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            PrependedText(
                'email', 
                '<i class="fa fa-envelope"></i>', 
                placeholder='Email Address (required)'
            ),
            PrependedText(
                'first_name',
                '<i class="fa fa-user"></i>', 
                placeholder='First Name (required)'
            ),
            PrependedText(
                'last_name',
                '<i class="fa fa-user"></i>', 
                placeholder='Last Name (required)'
            ),
            PrependedText(
                'password',
                '<i class="fa fa-key"></i>', 
                placeholder='Password (required)',
            ),
            Submit('submit', 'Register', css_class='btn-success btn-lg btn-block')
        )

    # Password Validation Check
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if validate_password(password, User) is not None:
            raise forms.ValidationError(_(password_validators_help_texts()))
        return password

    # Save User Model to Database
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
