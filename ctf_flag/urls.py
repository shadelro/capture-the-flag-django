# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.views.decorators.csrf import csrf_exempt

from dispatcher import dispatch


urlpatterns = patterns('',
    url(r'^/(?P<game_name>\w+)',
        csrf_exempt(dispatch(get='ctf_flag.views.get_flag')),
        name='get_flag'),
    )
