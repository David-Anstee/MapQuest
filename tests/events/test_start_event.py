from unittest import TestCase
from unittest.mock import patch

import events
from events import start_event


class Test(TestCase):
    @patch("events.get_event_sequence", side_effect=[{"0": {"xp": 4}}])
    @patch("events.run_event_stage", side_effect=["-1"])
    @patch('game.add_xp')
    def test_start_event_exits_gracefully(self, _, __, ___):
        game_state = {}
        tile_id = "AA"
        events.start_event(game_state=game_state, tile_id=tile_id)