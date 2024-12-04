"""
David Anstee
A01434810
"""
import json
from __init__ import LOCALISATION
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


def generate_location_description(game_state: dict[str: dict]) -> str:
    character = game_state["character"]
    board = game_state["board"]
    tile = board[(character["x_coord"], character["y_coord"])]
    return get_text("location_descriptions", tile["id"], True)


def get_stats(game_state: dict[str: dict]):
    character = game_state["character"]
    return f"Insight: {character["insight"]}\nMight: {character["might"]}\nCunning: {character["cunning"]}"


def main():
    example_text = get_text("intro", "0000", True)
    print(example_text)


if __name__ == "__main__":
    main()
