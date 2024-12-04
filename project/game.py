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

    game_state = state.make_game_state()
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
