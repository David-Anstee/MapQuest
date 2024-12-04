import random

import localisation
import player_input
import ui
from ui import describe_location


def make_tile(board: dict, coordinates: tuple, map_data: dict) -> dict:
    tile_terrain = map_data["regions"][str(coordinates[0])][str(coordinates[1])][0]
    tile_id = random.choice(map_data["tile_ids"][tile_terrain])
    map_data["tile_ids"][tile_terrain].remove(tile_id)

    new_tile = {"id": tile_id, "terrain": tile_terrain}

    return new_tile


def describe_game_state(game_state):
    board = game_state["board"]
    character = game_state["character"]
    world = game_state["world"]
    coordinates = (character["x_coord"], character["y_coord"])
    time_description = ui.style_text(text=localisation.get_text(namespace="time", loc_id=(str(world["time"]))),
                                      fore_colour=11, emphasis=5)
    terrain_description = ui.style_text(text=localisation.get_text(namespace="location",
                                                                    loc_id=board[coordinates]["terrain"]), fore_colour=14)
    day_description = f"Day {ui.style_text(text=str(world["day"]), fore_colour=14)}"
    day_description = f"{ui.style_text(day_description, emphasis=1)}"
    day_description = f"{ui.style_text(day_description, emphasis=4)}"
    print(f"{day_description}")
    #time.sleep(1.5)
    print(f"It is {time_description} in {terrain_description}")
    #time.sleep(3)
    print(f"You are {localisation.get_text("hp", str(character["hp"]))} ({str(character["hp"])} health).")
    #time.sleep(3)


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
    while True:
        movement = player_input.get_user_input(game_state)
        if player_input.move_is_valid(game_state, movement):
            break
    player_input.move_character(game_state, movement)


def arrive_at_tile(game_state):
    describe_location(game_state)


def journey_to_tile(game_state):
    ("You travel through")
