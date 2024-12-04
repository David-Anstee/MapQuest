from unittest import TestCase
from unittest.mock import patch

import tile
from game import make_board


class Test(TestCase):
    @patch("data.get_data", side_effect=[{}])
    @patch("tile.make_tile", side_effect=["meadow"])
    def test_make_board_dimensions_lower_boundary(self, _, __):
        board = make_board(1, 1)
        expected = 1
        actual = len(board)
        self.assertEqual(expected, actual)

    @patch("data.get_data", side_effect=[{}])
    @patch("tile.make_tile", side_effect=["meadow" for num in range(0, 25)])
    def test_make_board_dimensions_average_size(self, _, mock_response):
        board = make_board(5, 5)
        expected = 25
        actual = len(board)
        self.assertEqual(expected, actual)
