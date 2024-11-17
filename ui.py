"""
David Anstee
A01434810
"""


def get_colour(board: dict, coordinates: tuple) -> str:
    """
    Get the colour of a map tile.

    :param board: the game board the tile exists on
    :param coordinates: the coordinates of the tile
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
    tile_description = board[coordinates]
    colours = {"a peaceful meadow": "\033[1;32m", "a forest": "\033[0;32m", "a mountain": "\033[1;37m",
               "a plain": "\033[1;33m", "the side of a lake": "\033[0;34m"}

    return colours[tile_description]


def display_map(board: dict, character: dict):
    """
    Print a map representing the game board.

    :param board: the game board
    :param character: the player character
    :precondition: board is a dictionary where coordinates
                   are mapped to tile descriptions
    :precondition: character is a dictionary containing the
                   player's current coordinates
    :postcondition: Print the map

    >>> example_board = {(0, 0): "the side of a lake", (0, 1): "the side of a lake"}
    >>> example_character = {"x_coord": 0, "y_coord": 0, "visited_rooms": [(0, 0)]}
    >>> display_map(example_board, example_character) # doctest: +SKIP
    """
    map_display = ""
    max_row = max(key[0] for key in board.keys())
    max_col = max(key[1] for key in board.keys())

    for row in range(max_row+1):
        map_row = "\n"
        for column in range(max_col+1):
            coordinates = (row, column)
            assert coordinates in board

            if coordinates == (character["x_coord"], character["y_coord"]):
                map_row += "\033[1;35m*"
            elif coordinates in character["visited_rooms"]:
                map_row += get_colour(board, coordinates) + get_tile(board[coordinates])
            else:
                map_row += "?"
            map_row += "\033[0m "
        map_display += map_row
    print(map_display)


def describe_location(board: dict, character: dict):
    """
    Describe the player's current location.

    :param board: The game board
    :param character: The player character
    :precondition: board is a dictionary where coordinates
                   are mapped to tile descriptions
    :precondition: character is a dictionary containing the
                   player's current coordinates
    :postcondition: print a description of the player's current location

    >>> example_character = {'x_coord': 0, 'y_coord': 0}
    >>> example_board = {(0,0): "a peaceful meadow"}
    >>> describe_location(example_board, example_character)
    You arrive at a peaceful meadow
    """
    room_description = board[character["x_coord"], character["y_coord"]]
    print("You arrive at", room_description)


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
    if tile_description == "the side of a lake":
        return '≈'
    elif tile_description == "a forest":
        return '♣'
    elif tile_description == "a mountain":
        return '▲'
    elif tile_description == "a peaceful meadow":
        return ';'
    elif tile_description == "a plain":
        return 'l'
    else:
        return 'x'


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
