"""
David Anstee
A01434810
"""
from project import data, ui


def get_text(namespace: str, loc_id: str, new_line: bool = False) -> str:
    """
    Get text from localisation file.

    :param namespace: the namespace of the text
    :param loc_id: the id of the text
    :param new_line: whether to add new line before the text
    :precondition: namespace is a string corresponding to a namespace in the localisation file
    :precondition: loc_id is a string corresponding to an entry in the localisation file
    :precondition: new_line is a bool
    :postcondition: get the text from the localisation file
    :return: the text as a fstring
    """
    try:
        localisation = data.get_localisation()
    except FileNotFoundError:
        return "MISSING LOCALISATION FILE"

    output = f"\n" if new_line else f""
    try:
        output += f"{localisation[namespace][loc_id]}"
    except KeyError:
        return f"LOCALISATION NOT FOUND: {namespace}, {loc_id}"
    return output


def get_location_description(game_state: dict[str: dict]) -> str:
    """
    Get a location's unique description

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get the location's description
    :return: the location's description as a string
    """
    character = game_state["character"]
    board = game_state["board"]
    tile = board[(character["x_coord"], character["y_coord"])]
    return get_text("location_descriptions", tile["id"], True)


def get_stats(game_state: dict[str: dict]):
    """
    Get the player's stats

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get the player's stats
    :return: the player's stats as a fstring
    """
    character = game_state["character"]
    return f"Insight: +{character["insight"]}\nMight: +{character["might"]}\nCunning: +{character["cunning"]}"


def display_level_up_message(game_state: dict[str: dict]):
    """
    Display level up information.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: print level up information
    """
    character = game_state["character"]
    print(f"{get_text("info", "level_up", True)} {character["level"]}!")
    print(f"New stat levels:\n{get_stats(game_state=game_state)}")


def describe_game_state(game_state):
    """
    Describe the current game state.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: print information about the game state
    """
    board = game_state["board"]
    character = game_state["character"]
    world = game_state["world"]
    coordinates = (character["x_coord"], character["y_coord"])
    time_description = ui.style_text(text=get_text(namespace="time", loc_id=(str(world["time"]))),
                                     fore_colour=11, emphasis=5)
    terrain_description = ui.style_text(text=get_text(namespace="location",
                                        loc_id=board[coordinates]["terrain"]), fore_colour=14)
    day_description = f"Day {ui.style_text(text=str(world["day"]), fore_colour=14)}"
    day_description = f"{ui.style_text(day_description, emphasis=1)}"
    day_description = f"{ui.style_text(day_description, emphasis=4)}"
    print(f"{day_description}")
    print(f"It is {time_description} in {terrain_description}")
    print(f"You have {character["hp"]}/{character["max_hp"]} health.")


def get_quest_hint(game_state: dict[str: dict]) -> str:
    """
    Get a hint about the main quest.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get a quest hint
    :return: the quest hit as a string
    """
    character = game_state["character"]
    level = str(min(character["level"], 5))
    hint = get_text("hint", level)
    return hint


def get_reflection_text(game_state: dict[str: dict]) -> str:
    """
    Get reflection text.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get reflection text
    :return: the text as a string
    """
    character = game_state["character"]
    from project.ui import style_text
    text = (f"{style_text(text=character["name"], emphasis=1)}"
            f"\nLevel {character["level"]}, {character["xp"]}/{character["level"]*2} xp"
            f"\n\nHP: {character["hp"]}/{character["max_hp"]}"
            f"\n\n{get_stats(game_state=game_state)}"
            f"\n\nSupplies: {character["supplies"]}\nTrinkets: {character["trinkets"]}")
    text += f"\n\n{get_quest_hint(game_state=game_state)}"
    return text


def display_divider():
    """
    Print a divider.

    :postcondition: print a divider
    """
    print(f"\n─────────────────────────────────────────────────")


def get_consume_supplies_text(game_state: dict[str: dict]):
    """
    Get text for consuming supplies

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get text for consuming supplies
    :return: the text as a string
    """
    character = game_state["character"]
    text = (f"{get_text("info", "consume_supplies", True)}"
            f"\nRestored 2 hp (new hp: {min(character["hp"], character["max_hp"])})"
            f"\nConsumed 1 supplies (remaining: {character["supplies"]})")
    return text


def no_supplies_text(game_state: dict[str: dict]):
    """
    Get text for out of supplies

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: get text for out of supplies
    :return: the text as a string
    """
    character = game_state["character"]
    text = (f"{get_text("info", "no_supplies", True)}"
            f"\nLost 1 hp (new hp: {min(character["hp"], character["max_hp"])})")
    return text


def describe_new_tile(game_state):
    """
    Describe the current tile.

    :param game_state: the current game state
    :precondition: game_state is a well-formed dictionary
    :postcondition: print the description of the current tile
    """
    character = game_state["character"]
    coordinates = (character["x_coord"], character["y_coord"])
    if coordinates not in character["visited_rooms"]:
        print(get_location_description(game_state))
    else:
        print("You have been here before.")
