# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.views.decorators.csrf import csrf_exempt

from dispatcher import dispatch


urlpatterns = patterns('',
    url(r'^/create_game',
        csrf_exempt(dispatch(post='ctf_game.views.create_game')),
        name='create_game'),
    url(r'^/(?P<game_name>\w+)/add_player',
        csrf_exempt(dispatch(post='ctf_game.views.add_player')),
        name='add_player'),
    url(r'^/(?P<game_name>\w+)',
        csrf_exempt(dispatch(get='ctf_game.views.get_game')),
        name='get_game'),
    url(r'^/?$',
        csrf_exempt(dispatch(get='ctf_game.views.games')),
        name='games'),
    )
