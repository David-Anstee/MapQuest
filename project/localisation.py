"""
David Anstee
A01434810
"""
from project import data


def get_text(namespace: str, loc_id: str, new_line: bool = False) -> str:
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
    character = game_state["character"]
    board = game_state["board"]
    tile = board[(character["x_coord"], character["y_coord"])]
    return get_text("location_descriptions", tile["id"], True)


def get_stats(game_state: dict[str: dict]):
    character = game_state["character"]
    return f"Insight: +{character["insight"]}\nMight: +{character["might"]}\nCunning: +{character["cunning"]}"


def display_level_up_message(game_state: dict[str: dict]):
    character = game_state["character"]
    print(f"{get_text("info", "level_up", True)} {character["level"]}!")
    print(f"New stat levels:\n{get_stats(game_state=game_state)}")
    print(f"{character["xp"]}/{character["level"]*2} {get_text("info", "next_level")} {character["level"]+1}")


def get_quest_hint(game_state: dict[str: dict]) -> str:
    character = game_state["character"]
    level = str(min(character["level"], 5))
    hint = get_text("hint", level)
    return hint


def get_reflection_text(game_state: dict[str: dict]) -> str:
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
    print(f"\n─────────────────────────────────────────────────")


def main():
    example_text = get_text("intro", "0000", True)
    print(example_text)


if __name__ == "__main__":
    main()
