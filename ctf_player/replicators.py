# -*- coding: utf-8 -*-

from ctf_player.models import Player


def build_player(player_name, location_x, location_y):
    """Builds a user with the given attributes. If the required attributes are
    missing they will be defaulted."""

    player = Player()
    player.player_name = player_name
    player.location_x = location_x
    player.location_y = location_y
    player.save()

    return player
