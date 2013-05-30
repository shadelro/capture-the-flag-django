# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from ctf_flag.models import Flag
from ctf_game.models import Game
from ctf_player.models import Player


# @login_required
def get_game(request, game_name):
    game = Game.get_game_by_game_name(game_name)
    flag = Flag.get_flag_by_game_name(game_name)

    if not game or not flag:
        raise Http404

    response_data = {
        'game_name': game.game_name,
        'goal_x': game.goal_x,
        'goal_y': game.goal_y,
        'is_active': game.is_active,
        'players': game.player_list,
        'flag_x': flag.location_x,
        'flag_y': flag.location_y,
        'flag_held_by': flag.held_by
    }
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


# @login_required
def create_game(request):
    game_name = request.POST.get('game_name')
    default_x = request.POST.get('default_x')
    default_y = request.POST.get('default_y')
    goal_x = request.POST.get('goal_x')
    goal_y = request.POST.get('goal_y')
    if not Game.get_game_by_game_name(game_name):
        game = Game.create_game(game_name, [], goal_x, goal_y)
        flag = Flag.create_flag(game_name, default_x, default_y)

    return HttpResponse(simplejson.dumps({}), mimetype="application/json")

# @login_required
def add_player(request, game_name):
    game = Game.get_game_by_game_name(game_name)

    if not game:
        raise Http404

    player_name = request.POST.get('player_name')
    game.add_player_to_game(player_name)

    return HttpResponse(simplejson.dumps({}), mimetype="application/json")

# @login_required
def games(request):
    games = Game.objects.all()
    active_games = []
    inactive_games = []
    players = []
    for game in games:
        if game.is_active:
            active_games.append(game)
        else:
            inactive_games.append(game)
        for player in game.player_list:
            players.append(player)

    context = {
        'active_games': active_games,
        'inactive_games': inactive_games,
        'players': players
    }

    return render_to_response('ctf_game/games.html', context)
