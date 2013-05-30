# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.views.decorators.csrf import csrf_exempt

from dispatcher import dispatch


urlpatterns = patterns('',
    url(r'^/pick_up_flag/(?P<player_name>\w+)',
        csrf_exempt(dispatch(post='ctf_player.views.pick_up_flag')),
        name='pick_up_flag'),
    url(r'^/update_player_location/(?P<player_name>\w+)',
        csrf_exempt(dispatch(post='ctf_player.views.update_player_location')),
        name='update_player_location'),
    url(r'^/create_player',
        csrf_exempt(dispatch(post='ctf_player.views.create_player')),
        name='create_player'),
    url(r'^/(?P<player_name>\w+)/tag_nearest_player',
        csrf_exempt(dispatch(post='ctf_player.views.tag_nearest_player')),
        name='tag_nearest_player'),
    url(r'^/(?P<player_name>\w+)',
        csrf_exempt(dispatch(get='ctf_player.views.get_player')),
        name='get_player'),
    url(r'^/?$',
        csrf_exempt(dispatch(get='ctf_player.views.players')),
        name='players'),
    )
