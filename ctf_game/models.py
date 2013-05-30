# -*- coding: utf-8 -*-

import ast
import uuid

from django.db import models

from ctf_flag.models import Flag
from ctf_player.models import Player


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


class Game(models.Model):
    game_name = models.CharField(unique=True, max_length=100)
    goal_x = models.FloatField()
    goal_y = models.FloatField()
    is_active = models.BooleanField(default=False)
    player_list = ListField()
    winner = models.CharField(max_length=100)


    def __unicode__(self):
        return self.game_name


    def start_game(self):
        self.is_active = True
        self.save()


    def add_player_to_game(self, player_name):
        if player_name not in self.player_list:
            player = Player.get_player_by_player_name(player_name) or Player.create_player(player_name, self.game_name)
            player.add_game_to_player(self.game_name)
            self.player_list.append(player_name)
            self.save()

    def end_game(self, player):
        game.winner = player.player_name
        game.is_active = False
        game.save()

    @classmethod
    def create_game(cls, game_name, player_list, goal_x, goal_y):
        game = Game()
        game.game_name = game_name
        game.goal_x = goal_x
        game.goal_y = goal_y
        game.is_active = False
        game.player_list = player_list
        game.winner = ''
        game.save()

        for player_name in player_list:
            if not Player.get_player_by_player_name(player_name):
                player = Player.create_player(player_name, game_name)

        return game

    @classmethod
    def get_game_by_game_name(cls, game_name):
        return Game.get_game(game_name=game_name)

    @classmethod
    def get_game(cls, **kwargs):
        """Return player"""
        try:
            return Game.objects.get(**kwargs) 
        except Game.DoesNotExist:
            return None
