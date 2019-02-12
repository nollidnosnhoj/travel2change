from django.views.generic import CreateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth import(
    authenticate, get_user_model, login, logout
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.http import is_safe_url
from .forms import LoginForm, RegisterForm

def user_is_not_logged_in(user):
    return not user.is_authenticated()

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    login_url = "/"

    def form_valid(self, form):
        request = self.request
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super().form_invalid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/signup.html'
    success_url = '/account/login/'

def logout_view(request):
    logout(request)
    return redirect('/')