import random

from project import encounter, events, state, localisation, player_input, ui
from project.player_input import move_character, get_user_input
from project.ui import describe_location


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
    print(f"You have {character["hp"]}/{character["max_hp"]} health).")
    #time.sleep(3)


def describe_new_tile(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    if coordinates not in character["visited_rooms"]:
        print(localisation.get_location_description(game_state))
        #time.sleep(5)
    else:
        print("You have been here before.")
        #time.sleep(2)


def get_options(game_state):
    board = game_state["board"]
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    tile = board[coordinates]

    options = []
    if game_state["world"]["time"] < 6:
        options.append("travel")
    else:
        options.append("travel_disabled")

    options.append("camp")
    options.append("reflect")
    return options


def get_terrain_travel_time(terrain: str) -> int:
    travel_times = {"meadow": 1, "forest": 3, "swamp": 3, "tundra": 1, "valley": 2, "mountain": 4, "cavern": 3,
                    "pale": 4, "end": 4}
    try:
        return travel_times[terrain]
    except KeyError:
        print("Invalid terrain!")
        return 0


def start_camping(game_state: dict[str: dict]):
    character = game_state["character"]
    world = game_state["world"]

    options = []
    for time in range(world["time"]+1, 8):
        options.append(f"time_{time}")
    options.append("next_day")
    options.append("cancel")

    user_input = player_input.get_user_input(options=options)
    if user_input != "cancel":
        new_time = user_input.split("_")[1]
        new_time = int(new_time) if new_time.isnumeric() else 0
        start_day = world["day"]
        time_passed = state.set_time(game_state=game_state, new_time=new_time)
        if world["day"] > start_day:
            if character["supplies"] > 1:
                character["hp"] += 2
                character["supplies"] -= 1
                print(localisation.get_text("info", "consume_supplies", True))
                print(f"Restored 2 hp (new hp: {min(character["hp"], character["max_hp"])})")
                print(f"Consumed 1 supplies (remaining: {min(character["supplies"], 5)})")
            else:
                print(localisation.get_text("info", "no_supplies"))
                character["health"] -= 1
                print(f"Lost 1 health (remaining: {character["hp"]}/{character["max_hp"]}")
        else:
            character['hp'] += (time_passed // 4)
            print(f"You restored 2 hp while resting (new hp: {min(character["hp"], character["max_hp"])})")
        character['hp'] = min(character['hp'], character['max_hp'])
        player_input.get_user_input(["continue"])
        return True
    else:
        return False


def cancel_action():
    return False


def disabled_action(action: str):
    print(f"{localisation.get_text("prompt_info", "action")}")
    return False


def start_travelling(game_state: dict[str, dict]):
    movement = player_input.get_movement()
    if movement != 'cancel':
        direction = player_input.direction_from_input(movement)
        if player_input.move_is_valid(game_state=game_state, direction=direction):
            travel(game_state=game_state, direction=direction)
            return True
        else:
            print("cannot move there")
            return False
    else:
        return False


def travel(game_state: dict[str: dict], direction: list[int, int]):
    character = game_state["character"]
    world = game_state["world"]

    start_coord = (character["x_coord"], character["y_coord"])
    end_coord = (character["x_coord"] + direction[0], character["y_coord"] + direction[1])

    travel_time = calculate_travel_time(game_state=game_state, start_coord=start_coord, end_coord=end_coord)
    time_remaining = travel_time

    print("You begin to travel")
    input("Press enter to continue...")

    while time_remaining > 0:
        while world["time"] > 5:
            options = ["stop_to_camp"]
            print(f"It is {localisation.get_text("time", str(world["time"]))}")
            if world["time"] > 6 and not character["items"]["light"] > 0:
                print(f"There isn't enough light to see where you're going.")
            else:
                options.append("continue_travel")
                print(f"It may be dangerous to travel this late...")
            user_input = get_user_input(options=options)
            if user_input == "stop_to_camp":
                start_camping(game_state=game_state)
            elif user_input == "continue_travel":
                break

        state.pass_time(game_state=game_state, time_passed=1)
        time_remaining -= 1

        if encounter.roll_for_encounter():
            print(f"ENCOUNTER at {localisation.get_text("time", str(world["time"]))}")
            input("enter")

    move_character(game_state=game_state, direction=direction)
    terrain = game_state["board"][end_coord]["terrain"]
    print(f"You arrive in {localisation.get_text("location", terrain)}")


def reflect(game_state: dict[str: dict]):
    reflection_text = localisation.get_reflection_text(game_state=game_state)
    localisation.display_divider()
    print(reflection_text)
    localisation.display_divider()
    get_user_input(options=["continue"])


def do_action(game_state: dict[str: dict], user_input: str) -> bool:
    input_to_action = {"travel": start_travelling, "camp": start_camping, "reflect": reflect}
    try:
        action = input_to_action[user_input]
    except KeyError:
        print(f"Invalid action: {user_input}")
        return False
    return action(game_state)


def handle_input(game_state: dict[str: dict]):
    options = get_options(game_state)
    user_input = player_input.get_user_input(options=options)
    return do_action(game_state=game_state, user_input=user_input)


def tile_event(game_state: dict[str: dict]):
    print("\ntile_event")


def tile_start(game_state: dict[str:dict], new_tile: bool = True):
    character = game_state["character"]
    localisation.display_divider()
    if new_tile:
        describe_game_state(game_state)
        describe_new_tile(game_state)


def run_tile(game_state: dict[str: dict]):
    tile_start(game_state=game_state)

    character = game_state["character"]
    board = game_state["board"]
    coordinates = (character["x_coord"], character["y_coord"])
    if coordinates not in character["visited_rooms"]:
        events.start_event(game_state=game_state, tile_id=board[coordinates]["id"])
        character["visited_rooms"].append(coordinates)

    if character["items"]["map"]:
        ui.display_map(game_state, character["items"]["map"] > 1)
    while True:
        if handle_input(game_state=game_state):
            break
        tile_start(game_state=game_state, new_tile=False)


def calculate_travel_time(game_state: dict[str: dict], start_coord: (int, int), end_coord: (int, int)) -> int:
    board = game_state["board"]
    start_terrain = board[start_coord]["terrain"]
    end_terrain = board[start_coord]["terrain"]
    return get_terrain_travel_time(start_terrain) + get_terrain_travel_time(end_terrain)


def arrive_at_tile(game_state):
    describe_location(game_state)


def journey_to_tile(game_state):
    pass
