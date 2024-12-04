"""
David Anstee
A01434810
"""
import random
import time

from colorama import just_fix_windows_console

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


def get_stat_selection(prompt: str, valid_stats: list[str]) -> str:
    for number, stat in enumerate(valid_stats, 1):
        prompt += f"\n{number}. {localisation.get_text("stats", stat)}"
    num_selection = input(prompt)

    while not num_selection.isnumeric() or not (1 <= int(num_selection) <= len(valid_stats)):
        print(f"\nInvalid input. Please enter 1 - {len(valid_stats)}.")
        num_selection = input(prompt)

    stat = valid_stats[int(num_selection)-1]
    valid_stats.remove(stat)
    return stat


def make_character() -> dict:
    """
    Make the player character.

    :postcondition: creates the player character as a dict
                    where strings representing stats are mapped to
                    various values
    :return: the player character as a dictionary
    """
    character = {"x_coord": 0, "y_coord": 0, "max_hp": 5, "hp": 5, "level": 1, "xp": 0, "visited_rooms": [],
                 "insight": 0, "might": 0, "cunning": 0, "items": {"map": 1, "light": 0}}

    stats = ["insight", "might", "cunning"]
    primary_stat = get_stat_selection(localisation.get_text("prompt", "first_stat", True),
                                      stats)
    secondary_stat = get_stat_selection(localisation.get_text("prompt", "second_stat", True),
                                        stats)

    character[primary_stat] = 2
    character[secondary_stat] = 1

    print(f"{localisation.get_text("info", "stat_bonuses", True)} "
          f"\n{localisation.get_stats({"character": character})}")
    input(localisation.get_text("prompt", "continue", True))
    return character


def increase_stat(game_state: dict[str: dict], stat: str):
    character = game_state["character"]
    progression = (0, 1, 2, 3, 5, 8, 13)
    for level in progression:
        if level > character[stat]:
            character[stat] = level
            break


def add_xp(game_state: dict[str: dict], amount: int):
    character = game_state["character"]
    current_xp = character["xp"]
    new_xp = current_xp + amount
    print(f"Gained {new_xp} xp!")

    while new_xp >= character["level"] * 2:
        new_xp %= (character["level"] * 2)
        level_up_character(game_state=game_state)

    character["xp"] = new_xp
    print(f"Current level: {character["level"]}")
    print(f"Current xp: {new_xp}")
    print(f"xp needed for next level: {character["level"]*2}")


def level_up_character(game_state: dict):
    character = game_state["character"]
    character["level"] += 1

    stats = ("insight", "might", "cunning")
    for stat in stats:
        increase_stat(game_state, stat)
    print(localisation.get_text("info", "leveled_up"))


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


def pass_time(game_state: dict[str: dict], time_passed: int, stop_at_midnight: bool = False):
    world = game_state["world"]
    new_time = (world["time"] + time_passed)
    new_time = min(new_time, 7) if stop_at_midnight else new_time % 8
    set_time(game_state, new_time)


def set_time(game_state: dict[str: dict], new_time: int) -> int:
    if 7 < new_time < 0:
        raise ValueError

    world = game_state["world"]
    old_time = world["time"]
    world["time"] = new_time
    time_passed = new_time - old_time if new_time > old_time else new_time + (14 - old_time)
    if old_time > new_time or time_passed > 7:
        world["day"] += 1
    return time_passed


def game():
    """
    Drive the game.
    """
    just_fix_windows_console()
    input(get_text("intro", "0000"))

    game_state = {"board": make_board(5, 6), "character": make_character(), "world": {"time": 0, "day": 1}}
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
