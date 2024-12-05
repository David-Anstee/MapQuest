"""
David Anstee
A01434810
"""
from project.localisation import get_text


def move_is_valid(game_state: dict, direction: list) -> bool:
    """
    Determine whether a move is valid.

    :param game_state: the current game state
    :param direction: the direction of the move
    :precondition: game_state is a well-formed dictionary
    :precondition: direction is a list of two integers
    :postcondition: check if the move is valid
    :return: whether the move is valid as a boolean
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


def direction_from_input(user_input: str) -> list[int]:
    """
    Get direction from the user's input.

    :param user_input: the user's input
    :precondition: user_input is a string equal to
                  "n", "s", "e", "w" (case-insensitive)
    :postcondition: Get a direction
    :return: The direction as a list of two integers

    >>> example_input = "East"
    >>> direction_from_input(example_input)
    [0, 1]
    >>> example_input = "north"
    >>> direction_from_input(example_input)
    [-1, 0]
    """
    user_input = user_input.lower()

    direction = [0, 0]
    direction[0] += (user_input in ["north", "south"]) * ((-1) ** (user_input == "north"))
    direction[1] += (user_input in ["east", "west"]) * ((-1) ** (user_input == "west"))

    return direction


def get_movement():
    """
    Get the player's movement.

    :postcondition: get the player's movement
    :return: the movement as a string
    """
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
    """
    Get input from the user.

    :param options: the options to present to the user
    :param option_prompt: the prompt to present to the user
    :param prompt_namespace: the name space of the prompt
    :param option_namespace: the name space of the options
    :precondition: options is a non-empty list of strings
    :precondition: option_prompt is a string corresponding to an entry in the localisation file
    :precondition: prompt_namespace is a string corresponding to a namespace in the localisation file
    :precondition: option_namespace is a string corresponding to a namespace in the localisation file
    :postcondition: get the user's input
    :return: the option selected by the user as a string
    """
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
