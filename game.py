"""
David Anstee
A01434810
"""
from project import localisation, tile, state
from colorama import just_fix_windows_console


def game():
    """
    Drive the game.
    """
    input(localisation.get_text("intro", "0000"))

    game_state = state.make_game_state()
    while not state.should_quit(game_state):
        tile.play_tile(game_state)

    if game_state["character"]["hp"] > 0:
        print("Thanks for playing!")
    else:
        print("You died!")


def main():
    """
    Drive the program.
    """
    just_fix_windows_console()
    game()


if __name__ == "__main__":
    main()
