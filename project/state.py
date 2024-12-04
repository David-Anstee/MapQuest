from project import localisation, data, tile, player_input


def make_game_state():
    world = make_world()
    board = make_board(5, 5)
    character = make_character()

    game_state = {"world": world, "board": board, "character": character}
    return game_state


def make_world():
    return {"time": 0, "day": 1}


def make_board(rows: int, columns: int) -> dict:
    new_board = {}
    map_data = data.get_map_data(["map_data"])
    for row in range(rows):
        for column in range(columns):
            new_board[(row, column)] = tile.make_tile(new_board, (row, column), map_data)
    return new_board


def make_character() -> dict:
    """
    Make the player character.

    :postcondition: creates the player character as a dict
                    where strings representing stats are mapped to
                    various values
    :return: the player character as a dictionary
    """
    character = {"x_coord": 0, "y_coord": 0, "max_hp": 5, "hp": 5, "level": 1, "xp": 0, "visited_rooms": [],
                 "insight": 0, "might": 0, "cunning": 0, "items": {"map": 1, "light": 0, }, "supplies": 5, "trinkets": 0
                 }

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
    character = game_state["character"]
    progression = (0, 1, 2, 3, 5, 8, 13)
    for level in progression:
        if level > character[stat]:
            character[stat] = level
            break


def add_xp(game_state: dict[str: dict], amount: int):
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
    character = game_state["character"]
    character["level"] += 1

    stats = ("insight", "might", "cunning")
    for stat in stats:
        increase_stat(game_state, stat)
    localisation.display_level_up_message(game_state=game_state)


def pass_time(game_state: dict[str: dict], time_passed: int, stop_at_midnight: bool = False):
    world = game_state["world"]
    new_time = (world["time"] + time_passed)
    new_time = min(new_time, 7) if stop_at_midnight else new_time % 8
    set_time(game_state, new_time)


def set_time(game_state: dict[str: dict], new_time: int) -> int:
    if 7 < new_time < 0:
        raise ValueError

    world = game_state["world"]
    old_time = world["time"]
    world["time"] = new_time
    time_passed = new_time - old_time if new_time > old_time else new_time + (14 - old_time)
    if old_time > new_time or time_passed > 7:
        world["day"] += 1
    return time_passed


def should_quit(game_state: dict[str, dict]):
    return game_state["character"]["hp"] < 1
