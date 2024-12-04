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
    while not state.should_quit():
        tile.run_tile(game_state)


def main():
    """
    Drive the program.
    """
    just_fix_windows_console()
    game()


if __name__ == "__main__":
    main()
