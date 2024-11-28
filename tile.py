import random

import localisation
import player_input
import ui
from ui import describe_location


def make_tile(board: dict, coordinates: tuple, unused_tiles: dict) -> dict:
    new_tile = {}
    tile_type = ""
    tile_id = None
    if coordinates[0] + coordinates[1] < 3:
        tile_type = "meadow"
    elif coordinates == (0, 5):
        tile_type = "special"
        tile_id = "97"
    elif coordinates in [(0, 3), (1, 3)]:
        tile_type = "tundra"
    elif (coordinates[1] == 4 and coordinates[0] < 3) or coordinates == (1, 5):
        tile_type = "valley"
    elif (coordinates[0] + coordinates[1] < 5) or (coordinates[0] == 1) and (coordinates != (4, 0)):
        tile_type = "forest"
    elif 4 < (coordinates[0] + coordinates[1]) < 7 and (1 < coordinates[0] and 1 < coordinates[1] < 4):
        tile_type = "swamp"
    elif 6 < (coordinates[0] + coordinates[1]) < 9:
        tile_type = "mountain"
    elif coordinates == (4, 5):
        tile_type = "special"
        tile_id = "99"
    else:
        tile_type = "special"
        tile_id = "98"

    if tile_id is None:
        tile_id = random.choice(list(unused_tiles[tile_type]))

    print(coordinates, tile_type, tile_id)
    tile_data = unused_tiles[tile_type][tile_id]
    unused_tiles[tile_type].pop(tile_id)
    new_tile = tile_data
    new_tile["id"] = tile_id

    return new_tile


def describe_game_state(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    print(f"\nYou are in {localisation.get_text("location", board[coordinates]["terrain"])}")
    print(f"You are {localisation.get_text("hp", str(character["hp"]))} ({str(character["hp"])} health).")


def describe_new_tile(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    if coordinates not in character["visited_rooms"]:
        print(localisation.generate_location_description(game_state))
    else:
        print("You have been here before.")


def run_tile(game_state):
    ui.display_map(game_state)
    describe_game_state(game_state)
    describe_new_tile(game_state)
    movement = player_input.get_user_input(game_state)
    player_input.move_character(game_state, movement)


def arrive_at_tile(game_state):
    describe_location(game_state)


def journey_to_tile(game_state):
    ("You travel through")
