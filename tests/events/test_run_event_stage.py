from unittest import TestCase
from unittest.mock import patch
from project.events import run_event_stage


class Test(TestCase):
    @patch('events.apply_effects')
    @patch('player_input.get_user_input', side_effect=["choice_a"])
    @patch("events.get_next_stage", side_effect=["1"])
    def test_run_event_stage_returns_correct_stage(self, _, __, ___):
        expected = "1"
        actual = run_event_stage({}, {"description": "", "options": {"choice_a": "1"}})
        self.assertEqual(expected, actual)
