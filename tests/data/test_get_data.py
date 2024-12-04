from unittest import TestCase, mock
from unittest.mock import patch
from project import GAME_DATA, data


class Test(TestCase):
    @patch("project.data.get_data_file", side_effect=[GAME_DATA])
    def test_get_data_correct_data(self, _):
        expected = ["meadow"]
        actual = data.get_data(["map_data", "regions", "0", "0"])
        self.assertEqual(expected, actual)
