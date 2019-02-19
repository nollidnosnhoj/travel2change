from django import forms
from django.contrib.auth import (
    authenticate, get_user_model
)
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    PasswordResetForm
)
from django.contrib.auth.password_validation import (
    password_validators_help_text_html, validate_password
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

    # Authentication Validation
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError(_("This user is currently inactive."))
            else:
                raise forms.ValidationError(_("Email or Password is Incorrect."))

class RegisterForm(forms.ModelForm):

    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    # Password Validation Check
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if validate_password(password, User) is not None:
            raise forms.ValidationError(_(password_validators_help_text_html()))
        return password

    # Save User Model to Database
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            PrependedText(
                'email', 
                '<i class="fa fa-envelope"></i>', 
                placeholder='Email Address'
            ),
            Submit('submit', 'Reset Password', css_class='btn-success btn-lg btn-block')
        )