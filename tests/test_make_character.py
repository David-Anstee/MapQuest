from unittest import TestCase
from unittest.mock import patch
from project import state


class Test(TestCase):
    @patch("project.player_input.get_user_input", side_effect=["insight", "might"])
    @patch("project.localisation.get_text", side_effect=["", "", ""])
    def test_make_character_correct_primary_selection(self, _, __):
        character = state.make_character()
        expected = 2
        actual = character["insight"]
        self.assertEqual(expected, actual)

    @patch("project.player_input.get_user_input", side_effect=["insight", "might"])
    @patch("project.localisation.get_text", side_effect=["", "", ""])
    def test_make_character_correct_secondary_selection(self, _, __):
        character = state.make_character()
        expected = 1
        actual = character["might"]
        self.assertEqual(expected, actual)
