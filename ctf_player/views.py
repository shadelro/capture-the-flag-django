# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.utils import simplejson

from ctf_flag.models import Flag
from ctf_game.models import Game
from ctf_player.models import Player


# @login_required
def create_player(request):
    player_name = request.POST.get('player_name')
    if not Player.get_player_by_player_name(player_name):
        player = Player.create_player([], player_name)

    return HttpResponse(simplejson.dumps({}), mimetype="application/json")

# @login_required
def get_player(request, player_name):
    player = Player.get_player_by_player_name(player_name)

    if not player:
        return HttpResponse(content='player not found', status=404)

    response_data = {
        'location_x': player.location_x,
        'location_y': player.location_y,
        'player_name': player.player_name,
        'flags': player.flag_list,
        'games': player.game_list
    }
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

# @login_required
def update_player_location(request, player_name):
    player = Player.get_player_by_player_name(player_name)

    if not player:
        raise Http404

    location_x = request.POST.get('location_x')
    location_y = request.POST.get('location_y')

    player.update_location(location_x, location_y)

    return HttpResponse(simplejson.dumps({}), mimetype="application/json")

def pick_up_flag(request, player_name):
    player = Player.get_player_by_player_name(player_name)

    if not player:
        raise Http404

    game_name = request.POST.get('game_name')
    flag = Flag.get_flag_by_game_name(game_name)
    if abs(flag.location_x - player.location_x) < 1 and abs(flag.location_y - player.location_y) < 1:
        player.pick_up_flag(flag)
        return HttpResponse(simplejson.dumps({}), mimetype="application/json")

    raise HttpResponseBadRequest('can\'t reach')

def tag_nearest_player(request, player_name):
    player = Player.get_player_by_player_name(player_name)
    game_name = request.POST.get('game_name')
    game = Game.get_game_by_game_name(game_name)

    closest_player = None
    nearest = settings.TAG_RANGE
    for player_to_tag in game.player_list:
        if player_to_tag != player.player_name:
            distance = player.distance_to_player(player_to_tag)
            if distance < nearest:
                nearest = distance
                closest_player = player_to_tag
    if closest_player:
        player.tag_player(closest_player, game)

    return HttpResponse(simplejson.dumps({}), mimetype="application/json")

# @login_required
def players(request):
    players = Player.objects.all()
    context = {'players': players}

    return render_to_response('ctf_player/players.html', context)
