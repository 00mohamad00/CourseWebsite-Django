from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Account

from .forms import SignUpForm, LoginForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView


class LoginAccount(SuccessMessageMixin, LoginView):
    template_name = 'accountPanel/login.html'
    success_message = 'Welcome to your profile'


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'accountPanel/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your profile was created successfully"


class ChaneID(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['student_id']
    template_name = 'accountPanel/student_id.html'

    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
