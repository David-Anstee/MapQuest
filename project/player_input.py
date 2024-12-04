"""
David Anstee
A01434810
"""
from project.localisation import get_text


def move_is_valid(game_state: dict, direction: list) -> bool:
    """
    Determine whether a move is valid.

    :param board: The game board the move is happening on
    :param character: The character making the move
    :param direction: The direction the move is going
    :precondition: board is a dictionary where coordinate
                   are represented as tuples
    :precondition: character is a dictionary containing
                   the character's current coordinates
    :precondition: direction is a list where the first
                   element is an integer representing
                   the x-axis and the second element is
                   an integer representing the y-axis
    :postcondition: check if the move is valid
    :return: whether the move is valid as a boolean

    >>> example_board = {(0, 0): "a peaceful meadow", (0, 1): "a peaceful meadow"}
    >>> example_character = {"x_coord": 0, "y_coord": 0}
    >>> example_direction = [1, 0]
    >>> move_is_valid(example_board, example_character, example_direction)
    False
    >>> example_board = {(0, 0): "a peaceful meadow", (0, 1): "a peaceful meadow"}
    >>> example_character = {"x_coord": 0, "y_coord": 0}
    >>> example_direction = [0, 1]
    >>> move_is_valid(example_board, example_character, example_direction)
    True
    """
    character = game_state["character"]
    board = game_state["board"]
    max_row = max(key[0] for key in board.keys())
    max_col = max(key[1] for key in board.keys())
    return (0 <= character["x_coord"] + direction[0] <= max_row and
            0 <= character["y_coord"] + direction[1] <= max_col)


def move_character(game_state: dict, direction: list):
    """
    Move a character in the given direction.

    :param game_state: a dictionary
    :param direction: the direction the character is moving in
    :precondition: board is a dictionary where coordinates are keys
                   represented as tuples of non-negative integers
    :precondition: character is a dictionary containing the
                   character's current coordinates and a list of
                   previously visited coordinates
    :precondition: direction is a list containing two integers
    :precondition: moving in the given direction will not take
                   the character off the board
    :postcondition: the character moves in the given direction
    """
    character = game_state["character"]
    character["x_coord"] += direction[0]
    character["y_coord"] += direction[1]


def is_directional(user_input: str) -> bool:
    """
    Determine whether the user's input represents a direction.

    :param user_input: the user's input
    :precondition: user_input is a string
    :postcondition: determine whether the user's input is directional
    :return: a boolean representing whether the user's input is directional

    >>> example_input = "N"
    >>> is_directional(example_input)
    True
    >>> example_input = "Not a direction"
    >>> is_directional(example_input)
    False
    """
    return user_input.lower() in ["n", "s", "e", "w"]


def direction_from_input(user_input: str) -> list[int, int]:
    """
    Get direction from the user's input.

    :param user_input: the user's input
    :precondition: user_input is a string equal to
                  "n", "s", "e", "w" (case-insensitive)
    :postcondition: Get a direction
    :return: The direction as a list of two integers

    >>> example_input = "E"
    >>> direction_from_input(example_input)
    [0, 1]
    >>> example_input = "n"
    >>> direction_from_input(example_input)
    [-1, 0]
    """
    user_input = user_input.lower()

    direction = [0, 0]
    direction[0] += (user_input in ["north", "south"]) * ((-1) ** (user_input == "north"))
    direction[1] += (user_input in ["east", "west"]) * ((-1) ** (user_input == "west"))

    return direction


def get_movement():
    options = ["north", "south", "east", "west", "cancel"]
    while True:
        prompt = f"{get_text("prompt", "move", True)}"
        for number, option in enumerate(options, 1):
            prompt += f"\n{number}. {option}"
        user_input = input(prompt)
        if user_input.lower() in options:
            return user_input
        elif user_input.isnumeric() and 0 < int(user_input) <= len(options):
            return options[int(user_input)-1]
        else:
            print(get_text("error", "invalid_input", True))


def get_user_input(options: [str], option_prompt: str = "options",
                   prompt_namespace: str = "prompt", option_namespace: str = "prompt"):
    while True:
        prompt = f"{get_text(prompt_namespace, option_prompt, True)}"
        for number, option in enumerate(options, 1):
            prompt += f"\n{number}. {get_text(option_namespace, option)}"
        user_input = input(prompt+f"\n")
        if user_input.lower() in options:
            return user_input
        elif user_input.isnumeric() and 0 < int(user_input) <= len(options):
            return options[int(user_input)-1]
        else:
            print(get_text("error", "invalid_input", True))


# def prompt_user()


def main():
    """
    Drive the program.
    """
    board = {(0, 0): "a peaceful meadow", (0, 1): "the side of a lake"}
    character = {"x_coord": 0, "y_coord": 0, "visited_rooms": [(0, 0)]}
    get_user_input(board, character)


if __name__ == "__main__":
    main()
