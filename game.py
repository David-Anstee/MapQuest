"""
David Anstee
A01434810
"""
import random
import time

import data
import encounter
import localisation
from localisation import get_text
import ui
import player_input
import tile


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
    map_data = data.get_data(["map_data"])
    for row in range(rows):
        for column in range(columns):
            new_board[(row, column)] = tile.make_tile(new_board, (row, column), map_data)
    return new_board


def make_character() -> dict:
    """
    Make the player character.

    :postcondition: creates the player character as a dict
                    where strings representing stats are mapped to
                    various values
    :return: the player character as a dictionary
    """
    character = {"x_coord": 0, "y_coord": 0, "hp": 5, "level": 1, "visited_rooms": [],
                 "insight": 0, "might": 0, "cunning": 0}
    stats = ["insight", "might", "cunning"]

    primary_prompt = f"{localisation.get_text("prompt", "first_stat", True)}"
    for number, stat in enumerate(stats, 1):
        primary_prompt += f"\n{number}. {localisation.get_text("stats", stat)}"

    primary_stat = input(primary_prompt)
    while not primary_stat.isnumeric() or not int(primary_stat) in [1, 2, 3]:
        print("\nInvalid input. Please enter 1 - 3.")
        primary_stat = input(primary_prompt)
    primary_stat = stats[int(primary_stat)-1]
    stats.remove(primary_stat)

    secondary_prompt = f"{localisation.get_text("prompt", "second_stat", True)}"
    for number, stat in enumerate(stats, 1):
        secondary_prompt += f"\n{number}. {localisation.get_text("stats", stat)}"

    secondary_stat = input(secondary_prompt)
    while not secondary_stat.isnumeric() or not int(secondary_stat) in [1, 2]:
        print("\nInvalid input. Please enter 1 or 2.")
        secondary_stat = input(secondary_prompt)
    secondary_stat = stats[int(secondary_stat)-1]

    character[primary_stat] = 2
    character[secondary_stat] = 1

    print(f"{localisation.get_text("info", "stat_bonuses", True)} "
          f"\n{localisation.get_stats({"character": character})}")
    input(localisation.get_text("prompt", "continue", True))
    return character


def level_up_character(game_state: dict):
    character = game_state["character"]
    character["level"] += 1
    stat_progression = [0, 1, 2, 3, 5, 8, 13]
    new_stats = {"insight": 0, "might": 0, "cunning": 0}
    for num in enumerate(stat_progression):
        if character["insight"] == num[1] and num[1] < len(stat_progression):
            new_stats["insight"] = stat_progression[num[0] + 1]
        if character["might"] == num[1] and num[1] < len(stat_progression):
            new_stats["might"] = stat_progression[num[0] + 1]
        if character["cunning"] == num[1] and num[0] < len(stat_progression):
            new_stats["cunning"] = stat_progression[num[0] + 1]
    character["insight"] = new_stats["insight"]
    character["might"] = new_stats["might"]
    character["cunning"] = new_stats["cunning"]


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

    if total_roll >= target:
        return 2 + (total_roll >= target+6)
    else:
        return 1 - (total_roll <= target-6)


def game():
    """
    Drive the game.
    """
    input(get_text("intro", "0000"))

    game_state = {"board": make_board(5, 6), "character": make_character()}
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
