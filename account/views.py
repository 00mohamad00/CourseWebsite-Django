from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm


def base(request):
    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = None
    return render(request, 'account/base.html', context={'user': user})


def login_account(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            form = LoginForm()
    else:
        return Http404

    return render(request, 'accountPanel/login.html', context={'form': form})


def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            form = SignUpForm()

    else:
        return Http404

    return render(request, 'accountPanel/signup.html', context={'form': form})


def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')