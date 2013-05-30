# -*- coding: utf-8 -*-

import uuid

from django.db import models


class Flag(models.Model):
    game_name = models.CharField(unique=True, max_length=100)
    default_x = models.FloatField()
    default_y = models.FloatField()
    location_x = models.FloatField()
    location_y = models.FloatField()
    held_by = models.CharField(null=True, max_length=100)
    
    def __unicode__(self):
        return self.game_name

    def get_location(self):
        """Return x, y location."""
        return (self.location_x, self.location_y)

    def update_location(self, x, y):
        """Update x, y location."""
        self.location_x = x
        self.location_y = y
        self.save()

    def reset(self):
        self.location_x = self.default_x
        self.location_y = self.default_y
        self.held_by = ''
        self.save()
        
        
    @classmethod
    def create_flag(self, game_name, default_x, default_y):
        flag = Flag()
        flag.default_x = default_x
        flag.default_y = default_y
        flag.location_x = default_x
        flag.location_y = default_y
        flag.game_name = game_name
        flag.held_by = ''
        flag.save()
        return flag

    @classmethod
    def get_flag_by_game_name(cls, game_name):
        return Flag.get_flag(game_name=game_name)

    @classmethod
    def get_flag(cls, **kwargs):
        """Return flag"""
        try:
            return Flag.objects.get(**kwargs) 
        except Flag.DoesNotExist:
            return None
