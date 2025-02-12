from unittest import TestCase
from unittest.mock import patch
from project import events

class Test(TestCase):

    @patch('project.events.skill_check', side_effect=[True])
    def test_get_next_stage_skill_check_success(self, _):
        game_state = {}
        choice = {"skill_check": ["insight", 6], "success": "1", "failure": "2"}
        expected = "1"
        actual = events.get_next_stage(game_state=game_state, choice=choice)
        self.assertEqual(expected, actual)

    @patch('project.events.skill_check', side_effect=[False])
    def test_get_next_stage_skill_check_failure(self, _):
        game_state = {}
        choice = {"skill_check": ["insight", 6], "success": "1", "failure": "2"}
        expected = "2"
        actual = events.get_next_stage(game_state=game_state, choice=choice)
        self.assertEqual(expected, actual)

    def test_get_next_stage_skill_no_skill_check(self):
        game_state = {}
        choice = {"success": "1", "failure": "2"}
        expected = "1"
        actual = events.get_next_stage(game_state=game_state, choice=choice)
        self.assertEqual(expected, actual)
