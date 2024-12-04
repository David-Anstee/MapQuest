import __init__
import json


def get_map_data_file():
    return __init__.MAP_DATA


def get_event_data_file():
    return __init__.EVENT_DATA


def get_map_data(identifiers: list[str]):
    output = None
    with open(get_map_data_file(), 'r') as text_file:
        data = json.load(text_file)
        for name in identifiers:
            data = data[name]
        output = data
    return output


def get_event_data(tile_id: str) -> dict[str: ...]:
    with open(get_event_data_file(), 'r') as event_data:
        event_json = json.load(event_data)
        event_sequence = event_json["tile_events"][tile_id]
    return event_sequence


def main():
    example_data = get_map_data(["tiles", "early", "00"])
    print(example_data)


if __name__ == "__main__":
    main()
