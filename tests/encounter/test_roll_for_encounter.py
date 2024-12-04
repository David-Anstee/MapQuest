from unittest import TestCase
from unittest.mock import patch

from project.encounter import roll_for_encounter


class Test(TestCase):
    @patch('random.randint', side_effect=[1])
    def test_roll_for_encounter_success(self, _):
        self.assertTrue(roll_for_encounter())

    @patch('random.randint', side_effect=[10])
    def test_roll_for_encounter_narrow_success(self, _):
        self.assertTrue(roll_for_encounter())

    @patch('random.randint', side_effect=[100])
    def test_roll_for_encounter_failure(self, _):
        self.assertFalse(roll_for_encounter())

    @patch('random.randint', side_effect=[11])
    def test_roll_for_encounter_narrow_failure(self, _):
        self.assertFalse(roll_for_encounter())

    @patch('random.randint', side_effect=[40])
    def test_roll_for_encounter_success_with_different_rate(self, _):
        self.assertTrue(roll_for_encounter(encounter_rate=60))

    @patch('random.randint', side_effect=[80])
    def test_roll_for_encounter_failure_with_different_rate(self, _):
        self.assertFalse(roll_for_encounter(encounter_rate=60))

    def test_roll_for_encounter_guaranteed_success(self):
        self.assertTrue(roll_for_encounter(encounter_rate=100))

    def test_roll_for_encounter_guaranteed_failure(self):
        self.assertFalse(roll_for_encounter(encounter_rate=0))
