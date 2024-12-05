"""
David Anstee
A01434810
"""
COLOUR_RESET = "\033[0m"
COLOUR_FORE = "\033[38;5;"
COLOUR_BACK = "\033[48;5;"
TEXT_EMPHASIS = "\033["


def get_colour(terrain: str) -> str:
    """
    Get the colour of a terrain type.

    :param terrain: a terrain type
    :precondition: terrain is a string
    :precondition: terrain is a key in colours
    :postcondition: get the colour of the terrain
    :return: the colour as a string
    """
    colours = {"meadow": "\033[1;92m", "forest": "\033[38;5;22m", "mountain": "\033[1;90m",
               "swamp": "\033[38;5;65m"}
    try:
        return colours[terrain]
    except KeyError:
        return ""


def style_text(text: str, fore_colour: int = None, back_colour: int = None, emphasis: int = None) -> str:
    """
    Add style to text.

    :param text: the text to be styled
    :param fore_colour: the desired foreground colour
    :param back_colour: the desired background colour
    :param emphasis: the desired emphasis
    :precondition: text is a non-empty string
    :precondition: fore_colour is an integer between 0 and 255 (inclusive)
    :precondition: back_colour is an integer between 0 and 255 (inclusive)
    :precondition: emphasis is an integer between 0 and 10 (inclusive)
    :postcondition: style the text with foreground colour, background colour, and emphasis
    :return: the styled text as an f-string
    """
    foreground_colour = f"{COLOUR_FORE}{fore_colour}m" if fore_colour is not None else ""
    background_colour = f"{COLOUR_BACK}{back_colour}m" if back_colour is not None else ""
    emphasis = f"{TEXT_EMPHASIS}{emphasis}m" if emphasis is not None else ""

    return f"{emphasis}{foreground_colour}{background_colour}{text}{COLOUR_RESET}"


def display_map(game_state: dict[str, dict], map_size: int):
    """
    Display the map.

    :param game_state: the current game_state
    :param map_size: the size of the player's map
    :precondition: game_state is a well-formed string
    :precondition: map_size is a positive integer
    :postcondition: display the map
    """
    board = game_state["board"]
    character = game_state["character"]

    map_display = ""

    row_start = character["x_coord"] - map_size
    row_stop = character["x_coord"] + map_size

    column_start = character["y_coord"] - map_size
    column_stop = character["y_coord"] + map_size

    for row in range(row_start, row_stop+1):
        map_row = f"\n"
        for column in range(column_start, column_stop+1):
            coordinates = (row, column)
            if coordinates == (character["x_coord"], character["y_coord"]):
                map_row += "\033[1;35m*"
            elif (0 <= coordinates[0] <= max(key[0] for key in board.keys()) and
                  max(key[1] for key in board.keys()) >= 0 <= coordinates[1]):
                map_row += get_colour(board[coordinates]["terrain"]) + get_tile(board[coordinates]["terrain"])
            map_row += "\033[0m "
        map_display += map_row
    print(map_display)


def get_tile(terrain: str) -> str:
    """
    Get a terrain type's symbol.

    :param terrain: the terrain type
    :precondition: terrain type is a string
    :precondition: terrain type is a key in tile_icons
    :postcondition: get the terrain's symbol
    :return: The terrain's symbol as a string

    >>> get_tile("bad tile description")
    'x'
    >>> get_tile("a forest")
    '♣'
    """
    tile_icons = {"meadow": ";", "forest": "♣", "swamp": "\"", "mountain": "▲", "caverns": "○", "end": "!", "pale": "?",
                  "valley": "U", "tundra": "⎵"}
    try:
        return tile_icons[terrain]
    except KeyError:
        return "x"
