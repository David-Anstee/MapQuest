"""
David Anstee
A01434810
"""
import random
import time

import encounter
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
    character = {"x_coord": 0, "y_coord": 0, "hp": 5, "level": 1, "visited_rooms": [(0, 0)],
                 "insight": 0, "might": 0, "cunning": 0}
    primary_prompt = (f"Pick your primary stat:"
                      f"\n1. Insight - your intelligence and ability to notice things"
                      f"\n2. Might - your physical strength, and endurance"
                      f"\n3. Cunning - your deceptiveness and stealth")
    secondary_prompt = (f"\nPick your secondary stat:"
                        f"\n1. Insight - your intelligence and ability to notice things"
                        f"\n2. Might - your physical strength, and endurance"
                        f"\n3. Cunning - your deceptiveness and stealth")
    primary_stat = input(primary_prompt)
    while not primary_stat.isnumeric() or not (0 < int(primary_stat) < 4):
        print("\nInvalid input. Please enter a number from 1-3.")
        primary_stat = input(primary_prompt)
    primary_stat = int(primary_stat)

    secondary_stat = input(secondary_prompt)

    while not secondary_stat.isnumeric() or not (0 < int(secondary_stat) < 4):
        print("\nInvalid input. Please enter a number from 1-3.")
        secondary_stat = input(secondary_prompt)
    secondary_stat = int(secondary_stat)

    number_to_stat = {1: "insight", 2: "might", 3: "cunning"}
    primary_stat = number_to_stat[primary_stat]
    secondary_stat = number_to_stat[secondary_stat]
    character[primary_stat] = 2
    character[secondary_stat] = 1
    print(f"Your stats are:"
          f"\nInsight: {character["insight"]}"
          f"\nMight: {character["might"]}"
          f"\nCunning: {character["cunning"]}")

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

    game_state = {"board": make_board(5, 5), "character": make_character()}
    should_quit = False

    while not should_quit:
        input("type enter")


def main():
    """
    Drive the program.
    """
    game()


if __name__ == "__main__":
    main()
