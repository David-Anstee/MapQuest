from unittest import TestCase
from project.events import apply_effects


class Test(TestCase):
    def test_apply_effects_no_effects(self):
        game_state = {"character": {"hp": 5}}
        event_stage = {}
        apply_effects(game_state=game_state, event_stage=event_stage)
        expected = 5
        actual = game_state["character"]["hp"]
        self.assertEqual(expected, actual)

    def test_apply_effects_one_effect(self):
        game_state = {"character": {"hp": 5}}
        event_stage = {"effects": {"character": {"hp": -1}}}
        apply_effects(game_state=game_state, event_stage=event_stage)
        expected = 4
        actual = game_state["character"]["hp"]
        self.assertEqual(expected, actual)

    def test_apply_effects_multiple_effects(self):
        game_state = {"character": {"hp": 5, "xp": 3}}
        event_stage = {"effects": {"character": {"hp": -1, "xp": -1}}}
        apply_effects(game_state=game_state, event_stage=event_stage)
        expected = {"hp": 4, "xp": 2}
        actual = game_state["character"]
        self.assertDictEqual(expected, actual)
