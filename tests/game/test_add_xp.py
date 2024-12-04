from unittest import TestCase
from unittest.mock import patch
from game import add_xp


class Test(TestCase):
    def test_add_xp_correct_amount(self):
        game_state = {"character": {"xp": 0, "level": 1}}
        add_xp(game_state=game_state, amount=1)
        expected = 1
        actual = game_state["character"]["xp"]
        self.assertEqual(expected, actual)

    @patch("game.level_up_character")
    def test_add_xp_reduces_xp_on_level_up(self, _):
        game_state = {"character": {"xp": 0, "level": 1}}
        add_xp(game_state=game_state, amount=2)
        expected = 0
        actual = game_state["character"]["xp"]
        self.assertEqual(expected, actual)
