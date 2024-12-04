from unittest import TestCase
from unittest.mock import patch
from game import make_character


class Test(TestCase):
    @patch("game.get_stat_selection", side_effect=["insight", "might"])
    @patch("localisation.get_text", side_effect=["", "", ""])
    def test_make_character_correct_primary_selection(self, _, __):
        character = make_character()
        expected = 2
        actual = character["insight"]
        self.assertEqual(expected, actual)

    @patch("game.get_stat_selection", side_effect=["insight", "might"])
    @patch("localisation.get_text", side_effect=["", "", ""])
    def test_make_character_correct_secondary_selection(self, _, __):
        character = make_character()
        expected = 1
        actual = character["might"]
        self.assertEqual(expected, actual)
