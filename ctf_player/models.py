# -*- coding: utf-8 -*-

import ast
import uuid
from math import sqrt

from django.db import models

from ctf_flag.models import Flag


class ListField(models.TextField):
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)


class Player(models.Model):
    location_x = models.FloatField()
    location_y = models.FloatField()
    player_name = models.CharField(unique=True, max_length=100)
    flag_list = ListField()
    game_list = ListField()


    def __unicode__(self):
        return self.player_name

    def get_location(self):
        """Return x, y location."""
        return (self.location_x, self.location_y)

    def add_game_to_player(self, game_name):
        if game_name not in self.game_list:
            self.game_list.append(game_name)
            self.save()

    
    def distance_to_player(self, player_name):
        player = Player.get_player_by_player_name(player_name)
        return sqrt(pow(abs(self.location_x - player.location_x), 2) + pow(abs(self.location_y - player.location_y), 2))

    
    def tag_player(self, player_name, game):
        player_to_tag = Player.get_player_by_player_name(player_name)

        if game.game_name in player_to_tag.flag_list:
            player_to_tag.drop_flag(game.game_name)


    def update_location(self, x, y):
        """Update x, y location."""
        self.location_x = x
        self.location_y = y
        self.save()

        for game_name in self.flag_list:
            flag = Flag.get_flag_by_game_name(game_name)
            flag.update_location(x, y)
            if flag.is_in_goal():
                game = Game.get_game_by_game_name(game_name)
                game.end_game(self)

    def pick_up_flag(self, flag):
        """Pick up flag"""
        if not (flag.game_name in self.flag_list or flag.held_by):
            self.flag_list.append(flag.game_name)
            self.save()
            flag.held_by = self.player_name
            flag.save()

    def drop_flag(self, game_name):
        """Drop flag"""
        flag = Flag.get_flag_by_game_name(game_name)
        flag.reset()
        self.flag_list.remove(game_name)

    @classmethod
    def create_player(cls, player_name, game_name=None):
        player = Player()
        player.location_x = 0
        player.location_y = 0
        player.player_name = player_name
        player.has_flag = False
        player.game_list = []
        if game_name:
            player.game_list.append(game_name)
        player.save()

        return player

    @classmethod
    def get_player_by_player_name(cls, player_name):
        """Return player by player_name or None."""
        kwargs = {}
        kwargs['player_name'] = player_name
        return Player.get_player(**kwargs)

    @classmethod
    def get_player(cls, **kwargs):
        """Return player"""
        try:
            return Player.objects.get(**kwargs) 
        except Player.DoesNotExist:
            return None
