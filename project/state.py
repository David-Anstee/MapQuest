from project import localisation, data, player_input
import random


def make_game_state():
    """
    Make the game state.

    :postcondition: make the game state as a well-formed dictionary

    :postcondition: game_state contains a key "character" mapped to a well-formed dictionary
    :postcondition: game_state contains a key "board" mapped to a well-formed dictionary
    :postcondition: game_state contains a key "world" mapped to a well-formed dictionary
    :return: the game state as a dictionary
    """
    world = make_world()
    board = make_board(5, 6)
    character = make_character()

    if world["difficulty"] == "easy":
        character["supplies"] += 5
        character["max_hp"] += 2
        character["hp"] += 2

    game_state = {"world": world, "board": board, "character": character}
    return game_state


def make_world():
    """
    Make the world.

    :postcondition: make the world as a well-formed dictionary
    :return: the world as a dictionary
    """
    difficulty_options = ["easy", "normal"]
    difficulty = player_input.get_user_input(options=difficulty_options, option_prompt="difficulty")
    return {"time": 0, "day": 1, "difficulty": difficulty, "finished": False}


def make_tile(coordinates: tuple, map_data: dict) -> dict:
    """
    Make a tile.

    :param coordinates: the coordinates of the tile
    :param map_data: the data for the map
    :precondition: coordinates is a tuple containing two integers
    :precondition: coordinates corresponds to an entry in map_data
    :precondition: map_data is a well-formed dictionary
    :postcondition: make the tile as a well-formed dictionary
    :return: the tile as a dictionary
    """
    tile_terrain = map_data["regions"][str(coordinates[0])][str(coordinates[1])][0]
    tile_id = random.choice(map_data["tile_ids"][tile_terrain])
    map_data["tile_ids"][tile_terrain].remove(tile_id)

    new_tile = {"id": tile_id, "terrain": tile_terrain}

    return new_tile


def make_board(rows: int, columns: int) -> dict:
    """
    Make the game board.

    :param rows: the number of rows on the board
    :param columns: the number of columns on the board
    :precondition: rows is a positive integer
    :precondition: columns is a positive integer
    :postcondition: make the game board
    :return: the game board as a dictionary
    """
    new_board = {}
    map_data = data.get_map_data(["map_data"])
    for row in range(rows):
        for column in range(columns):
            new_board[(row, column)] = make_tile((row, column), map_data)
    return new_board


def make_character() -> dict:
    """
    Make the player character.

    :postcondition: creates the player character as a well-formed dictionary
    :return: the player character as a dictionary
    """
    character = {"x_coord": 0, "y_coord": 0, "max_hp": 5, "hp": 5, "level": 1, "xp": 0, "visited_rooms": [],
                 "insight": 0, "might": 0, "cunning": 0, "map": 0, "supplies": 5, "trinkets": 0}

    stats = ["insight", "might", "cunning"]
    name_input = input("What is your name?\n").strip()
    character["name"] = name_input

    primary_stat = player_input.get_user_input(options=stats, option_prompt="first_stat", option_namespace="stats")
    stats.remove(primary_stat)
    secondary_stat = player_input.get_user_input(options=stats, option_prompt="second_stat", option_namespace="stats")

    character[primary_stat] = 2
    character[secondary_stat] = 1

    print(f"{localisation.get_text("info", "stat_bonuses", True)} "
          f"\n{localisation.get_stats({"character": character})}")
    return character


def increase_stat(game_state: dict[str: dict], stat: str):
    """
    Increase the player's stats.

    :param game_state: the current game state
    :param stat: the stat to be increased
    :precondition: game_state is a well-formed dictionary
    :precondition: stat is a string corresponding to a character stat
    :postcondition: increase the stat
    """
    character = game_state["character"]
    progression = (0, 1, 2, 3, 5, 8, 13)
    for level in progression:
        if level > character[stat]:
            character[stat] = level
            break


def add_xp(game_state: dict[str: dict], amount: int):
    """
    Add xp to the character.

    :param game_state: the current game state
    :param amount: the amount of xp
    :precondition: game_state is a well-formed dictionary
    :precondition: amount is a positive integer
    :postcondition: add the xp to the character
    """
    character = game_state["character"]
    current_xp = character["xp"]
    new_xp = current_xp + amount
    print(f"Gained {new_xp} xp!")

    while new_xp >= character["level"] * 2:
        new_xp %= (character["level"] * 2)
        level_up_character(game_state=game_state)

    character["xp"] = new_xp
    print(f"Current xp: {new_xp}/{character["level"]*2}")


def level_up_character(game_state: dict):
    """
    Level up the character.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: level up the character
    """
    character = game_state["character"]
    character["level"] += 1

    stats = ("insight", "might", "cunning")
    for stat in stats:
        increase_stat(game_state, stat)
    localisation.display_level_up_message(game_state=game_state)


def pass_time(game_state: dict[str: dict], time_passed: int):
    """
    Pass time.

    :param game_state: the current game state
    :param time_passed: the time passed
    :precondition: game state is a well_formed dictionary
    :precondition: time_passed is a positive integer
    :postcondition: pass the given amount of time, up to 7
    """
    world = game_state["world"]
    new_time = (world["time"] + time_passed)
    new_time = min(new_time, 7)
    set_time(game_state, new_time)


def set_time(game_state: dict[str: dict], new_time: int) -> int:
    """
    Set the time.

    :param game_state: the current game state
    :param new_time: the new time to be set
    :precondition: game_state is a well-formed dictionary
    :precondition: new_time is an integer between 0 and 7 (inclusive)
    :postcondition: set the time
    """

    world = game_state["world"]
    old_time = world["time"]
    world["time"] = new_time
    time_passed = new_time - old_time if new_time > old_time else new_time + (14 - old_time)
    if old_time > new_time or time_passed > 7:
        world["day"] += 1
    return time_passed


def should_quit(game_state: dict[str, dict]):
    """
    Determine whether the game should quit.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: determine if the game should quit
    :return: whether the game should quit as a bool
    """
    return game_state["character"]["hp"] < 1 or game_state["world"]["finished"]
