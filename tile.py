import random

import localisation
import player_input
import ui
from ui import describe_location


def make_tile(board: dict, coordinates: tuple, unused_tiles: dict) -> dict:
    new_tile = {}
    if coordinates[0] + coordinates[1] < 3:
        tile_id = random.choice(list(unused_tiles["early"]))
        tile_data = unused_tiles["early"][tile_id]

        unused_tiles["early"].pop(tile_id)
        new_tile = tile_data
        new_tile["id"] = tile_id
    else:
        new_tile = None
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
