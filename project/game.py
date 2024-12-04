"""
David Anstee
A01434810
"""
import random
import time
from colorama import just_fix_windows_console
import data
import localisation
import tile
from project import state


def make_board(rows: int, columns: int) -> dict:
    new_board = {}
    map_data = data.get_map_data(["map_data"])
    for row in range(rows):
        for column in range(columns):
            new_board[(row, column)] = tile.make_tile(new_board, (row, column), map_data)
    return new_board


def skill_check(game_state: dict, target: int, stat=None, drama=True) -> int:
    character = game_state["character"]
    modifier = 0 if (stat is None) else character[stat]
    print("Rolling dice...")
    if drama:
        time.sleep(1)
    first_roll = random.randint(1, 6)
    print(first_roll)

    if drama:
        time.sleep(2)
    second_roll = random.randint(1, 6)
    print(second_roll)
    if drama:
        time.sleep(1.5)
    print(f"Rolled {first_roll} + {second_roll} = {first_roll+second_roll}.")
    total_roll = first_roll + second_roll + modifier

    if modifier != 0:
        if drama:
            time.sleep(1.5)
        print(f"Modifier ({stat.title()}): {modifier}")
    if drama:
        time.sleep(1.5)
    print(f"Total roll: {total_roll}")

    return total_roll >= target


def game():
    """
    Drive the game.
    """
    just_fix_windows_console()
    input(localisation.get_text("intro", "0000"))

    game_state = {"board": make_board(5, 6), "character": state.make_character(), "world": {"time": 0, "day": 1}}
    should_quit = False

    while not should_quit:
        tile.run_tile(game_state)


def main():
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
