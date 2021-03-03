from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect


@login_required
def index(request):
    title = 'hassani good boy'
    return render(request, 'panel/index.html', context={'user': request.user, 'title': title})