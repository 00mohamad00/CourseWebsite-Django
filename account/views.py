from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import SignUpForm


def base(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            print('user is student')
        else:
            print('user is teacher')
        user = request.user.username
    else:
        user = None
    return render(request, 'panel/base.html', context={'user': user})


def login(request):
    pass


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
            return redirect('base')
        else:
            form = SignUpForm()

    else:
        return Http404

    return render(request, 'panel/signup.html', context={'form': form})

def teacher_panel(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return Http404
        else:
            return render(request, 'panel/base.html', context={'user': request.user})
    else:
        redirect('login')