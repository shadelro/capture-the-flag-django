# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import Http404

from ctf_flag.models import Flag


# @login_required
def get_flag(request, game_name):
    flag = Flag.get_flag_by_game_name(game_name)

    if not flag:
        raise Http404

    response_data = {
        'x_pos': flag.location_x,
        'y_pos': flag.location_y,
        'is_held': flag.is_held
    }

    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
