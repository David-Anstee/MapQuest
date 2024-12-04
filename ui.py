"""
David Anstee
A01434810
"""
from localisation import get_text
COLOUR_RESET = "\033[0m"
COLOUR_FORE = "\033[38;5;"
COLOUR_BACK = "\033[48;5;"
TEXT_EMPHASIS = "\033["


def get_colour(terrain: str) -> str:
    """
    Get the colour of a map tile.

    :param tile_name: the game board the tile exists on
    :precondition: board is a dictionary where coordinates
                   are mapped to tile descriptions
    :precondition: coordinates is a tuple containing
                   two non-negative integers
    :postcondition: get the colour of the tile
    :return: the colour of the tile as a string containing an escape sequence

    >>> example_board = {(0, 0): "the side of a lake"}
    >>> colour = get_colour(example_board, (0, 0))
    >>> colour == '\033[0;34m'
    True
    """
    colours = {"meadow": "\033[1;92m", "forest": "\033[38;5;22m", "mountain": "\033[1;90m",
               "swamp": "\033[38;5;65m"}
    try:
        return colours[terrain]
    except KeyError:
        return ""


def style_text(text: str, fore_colour: int = None, back_colour: int = None, emphasis: int = None) -> str:
    foreground_colour = f"{COLOUR_FORE}{fore_colour}m" if fore_colour is not None else ""
    background_colour = f"{COLOUR_BACK}{back_colour}m" if back_colour is not None else ""
    emphasis = f"{TEXT_EMPHASIS}{emphasis}m" if emphasis is not None else ""

    return f"{emphasis}{foreground_colour}{background_colour}{text}{COLOUR_RESET}"

    >>> example_board = {(0, 0): "the side of a lake", (0, 1): "the side of a lake"}
    >>> example_character = {"x_coord": 0, "y_coord": 0, "visited_rooms": [(0, 0)]}
    >>> display_map(example_board, example_character) # doctest: +SKIP
    """
    board = game_state["board"]
    character = game_state["character"]

    map_display = ""
    max_row = max(key[0] for key in board.keys())
    max_col = max(key[1] for key in board.keys())

    for row in range(max_row+1):
        map_row = "\n"
        for column in range(max_col+1):
            coordinates = (row, column)
            assert coordinates in board

            if coordinates == (character["x_coord"], character["y_coord"]):
                map_row += "\033[1;35m☺"
            elif True: # coordinates in character["visited_rooms"]:
                map_row += get_colour(board[coordinates]["terrain"]) + get_tile(board[coordinates]["terrain"])
            else:
                map_row += "?"
            map_row += "\033[0m "
        map_display += map_row
    print(map_display)


def describe_location(game_state: dict):
    """
    Describe the player's current location.

    :param game_state: an empty dictionary
    :precondition: board is a dictionary where coordinates
                   are mapped to tile descriptions
    :precondition: character is a dictionary containing the
                   player's current coordinates
    :postcondition: print a description of the player's current location
    """
    board = game_state["board"]
    coordinates = (game_state["character"]["x_coord"], game_state["character"]["y_coord"])
    tile_name = board[coordinates]
    print("You travel through the", get_text("location", tile_name))


def get_tile(tile_description: str) -> str:
    """
    Get a tile's symbol.

    :param tile_description: the description of the tile
    :precondition: tile_description is a string
    :postcondition: get the tile's symbol
    :return: The tile's symbol as a string

    >>> get_tile("bad tile description")
    'x'
    >>> get_tile("a forest")
    '♣'
    """
    tile_icons = {"meadow": ";", "forest": "♣", "swamp": "\"", "mountain": "▲", "caverns": "○", "end": "!", "pale": "?",
                  "valley": "U", "tundra": "⎵"}
    try:
        return tile_icons[tile_description]
    except KeyError:
        return "x"


def main():
    """
    Drive the program.
    """
    board = {(0, 0): "a peaceful meadow", (0, 1): "the side of a lake"}
    character = {"x_coord": 0, "y_coord": 0, "visited_rooms": [(0, 0)]}
    display_map(board, character)
    describe_location(board, character)


if __name__ == "__main__":
    main()
