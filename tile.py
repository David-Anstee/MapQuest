import localisation
import ui
from ui import describe_location


def describe_game_state(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    print(f"\nYou are in {localisation.get_text("location", board[coordinates])}")
    print(f"You are {localisation.get_text("hp", str(character["hp"]))} ({str(character["hp"])} health).")


def describe_new_tile(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    if coordinates not in (character["visited_locations"]):
        print(localisation.generate_location_description(game_state))
    else:
        print("You have been here before.")


def run_tile(game_state):
    ui.display_map(game_state)
    describe_game_state(game_state)
    describe_new_tile(game_state)
    input()


def arrive_at_tile(game_state):
    describe_location(game_state)


def journey_to_tile(game_state):
    ("You travel through")
