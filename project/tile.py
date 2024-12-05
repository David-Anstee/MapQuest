from project import events, localisation, ui, action, state


def get_terrain_travel_time(terrain: str) -> int:
    """
    Get travel time.

    :param terrain: a terrain type
    :precondition: terrain is a string
    :precondition: terrain is a key in travel_times
    :postcondition: get the terrain's travel time.
    :return: the travel time as an integer
    """
    travel_times = {"meadow": 1, "forest": 2, "swamp": 2, "tundra": 1, "valley": 2, "mountain": 3, "cavern": 2,
                    "pale": 3, "end": 3}
    try:
        return travel_times[terrain]
    except KeyError:
        print("Invalid terrain!")
        return 0


def tile_start(game_state: dict[str:dict], new_tile: bool = True):
    """
    """
    localisation.display_divider()
    if new_tile:
        localisation.describe_game_state(game_state)
        localisation.describe_new_tile(game_state)


def tile_visited(game_state: dict[str: dict]) -> bool:
    """
    Check if tile has been visited.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: check if the tile is visited
    :return: whether the tile has been visited as a bool
    """
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])

    return coordinates in character["visited_rooms"]


def play_tile(game_state: dict[str: dict]):
    """
    Play the tile.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: play the tile
    """
    tile_start(game_state=game_state)

    character = game_state["character"]
    board = game_state["board"]

    coordinates = (character["x_coord"], character["y_coord"])
    if not tile_visited(game_state=game_state):
        character["visited_rooms"].append(coordinates)
        events.start_event(game_state=game_state, tile_id=board[coordinates]["id"])

    if character["map"]:
        try:
            ui.display_map(game_state, character["map"])
        except KeyError:
            print("No map")

    while not state.should_quit(game_state=game_state):
        if action.handle_input(game_state=game_state):
            break
        tile_start(game_state=game_state, new_tile=False)


def calculate_travel_time(game_state: dict[str: dict], start_coord: (int, int), end_coord: (int, int)) -> int:
    """
    Calculate travel time.

    :param game_state: the current game state
    :param start_coord: the starting coordinates
    :param end_coord: the ending coordinate
    :precondition: game_state is a well-formed dictionary
    :precondition: start_coord is a tuple containing two ints
    :precondition: end_coord is a tuple containing two ints
    :postcondition: calculate the time to travel from start_coord to end_coord
    :return: the travel time as int
    """
    board = game_state["board"]
    start_terrain = board[start_coord]["terrain"]
    end_terrain = board[end_coord]["terrain"]
    return get_terrain_travel_time(start_terrain) + get_terrain_travel_time(end_terrain)
