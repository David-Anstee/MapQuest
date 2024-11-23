"""
David Anstee
A01434810
"""
import random

import encounter
from localisation import get_text
import ui
import player_input


def make_board(rows: int, columns: int) -> dict:
    """
    Make the game board.

    :param rows: the width of the board
    :param columns: the height of the board
    :precondition: rows is a positive integer
    :precondition: columns is a positive integer
    :postcondition: creates a dict representing the game board,
                    where tuples representing xy coordinates are
                    mapped to strings representing tile descriptions
    :return: the board as a dictionary of tuple:string

    >>> make_board(3, 3) # doctest: +SKIP
    {(0, 0): 'a mountain', (0, 1): 'a mountain', (0, 2): 'a forest', (1, 0): 'the side of a lake',
    (1, 1): 'a peaceful meadow', (1, 2): 'a plain', (2, 0): 'a forest', (2, 1): 'the side of a lake',
    (2, 2): 'a mountain'}
    """
    new_board = {}
    tiles = ["meadow", "forest", "swamp", "mountain"]
    for row in range(rows):
        for column in range(columns):
            new_board[(row, column)] = random.choice(tiles)
    return new_board


def make_character() -> dict:
    """
    Make the player character.

    :postcondition: creates the player character as a dict
                    where strings representing stats are mapped to
                    various values
    :return: the player character as a dictionary
    """
    character = {"x_coord": 0, "y_coord": 0, "hp": 5, "level": 1, "visited_rooms": [(0, 0)]}
    return character


def game():
    """
    Drive the game.
    """
    board = make_board(5, 5)
    character = make_character()

    input(get_text("intro", "0000"))
    while True:
        ui.display_map(board, character)
        ui.describe_location(board, character)

        movement = player_input.get_user_input(board, character)
        if not player_input.move_is_valid(board, character, movement):
            print(get_text("error", "bad_move", True))
            continue

        player_input.move_character(board, character, movement)
        if encounter.roll_for_encounter():
            encounter.start_encounter(board, character)


def main():
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
