# -*- coding: utf-8 -*-

from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from dispatcher import dispatch


urlpatterns = patterns('',
    url(r'^/?$',
        dispatch(get='views.home'),
        name='home'),
    url(r'login',
        dispatch(get='views.glogin',
                 post='views.plogin'),
        name='login'),
    url(r'logout',
        dispatch(get='views.glogout'),
        name='logout'),
    (r'flags', include('ctf_flag.urls')),
    (r'games', include('ctf_game.urls')),
    (r'players', include('ctf_player.urls')),
    url(r'signup',
        dispatch(get='views.gsignup',
                 post='views.psignup'),
        name='signup'),
    )
