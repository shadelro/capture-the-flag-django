# -*- coding: utf-8 -*-

import hashlib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response

from ctf_game.models import Game
from forms import LoginForm
from forms import SignupForm


def home(request):
    context = {}

    return render_to_response('index.html', context)


def glogin(request):
    if request.user.is_authenticated():
        redirect('/games')
    else:
        form = LoginForm()
        context = {'form':form}
        next = request.GET.get('next', None)
        if next:
            form.initial = {'next':next}

        return render_to_response('login.html', context)

def plogin(request):
    context = dict()
    form = LoginForm(request.POST)
    context['form'] = form
    next = form.data.get('next')

    if form.is_valid():
        username = form.cleaned_data.get('login_username')
        password = form.cleaned_data.get('login_password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next or reverse('games'))

    return render_to_response('login.html', context)

def glogout(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('/')

def gsignup(request):
    if request.user.is_authenticated():
        redirect(reverse('games'))
    else:
        form = SignupForm()
        context = {'form': form}
        next = request.GET.get('next', None)
        if next:
            form.initial = {'next': next}

        return render_to_response('signup.html', context)

def psignup(request):
    context = dict()
    form = SignupForm(request.POST)
    context['form'] = form
    next = form.data.get('next')

    if form.is_valid():
        return redirect(next or reverse('games'))

    return render_to_response('signup.html', context)
