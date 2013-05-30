# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from ctf_player.models import Player
from ctf_player.replicators import build_player


class PlayerViewTests(TestCase):
    """Ensure Player view works correctly."""

    def setUp(self):
        self.player = build_player(player_name='test',
                                   location_x='123.123',
                                   location_y='321.321')

    def test_update_player_location(self):
        """Functional: posting to update_player_location should update the x, y
        location of the player."""
        post_data = {
            'location_x': '234.234',
            'location_y': '432.432'
        }
        response = self.client.post(reverse('update_player_location',
                                            args=[self.player.player_name]),
                                    post_data)

        player = Player.get_player_by_player_name(self.player.player_name)
        self.assertEqual(player.location_x, u'234.234')
        self.assertEqual(player.location_y, u'432.432')

    def test_get_player(self):
        """Functional: performing a get on get_player should return the
        player."""
        response = self.client.get(reverse('get_player',
                                            args=[self.player.player_name]))

        
        self.assertEqual(response.status_code, 200)
        player = json.loads(response.content)
        self.assertEqual(player['player_name'], 'test')
        self.assertEqual(player['location_x'], u'123.123')
        self.assertEqual(player['location_y'], u'321.321')

    def test_get_player_404(self):
        """Functional: performing a get on get_player with a nonexistant player
        should return a 404."""
        response = self.client.get(reverse('get_player',
                                            args=['invalid']))

        
        self.assertEqual(response.status_code, 404)
