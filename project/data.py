import project as __init__
import json


def get_map_data_file():
    """
    Get the directory of the map data file.

    :postcondition: get the directory of the file
    :return: the directory as a string
    """
    return __init__.MAP_DATA


def get_event_data_file():
    """
    Get the directory of the event data file.

    :postcondition: get the directory of the file
    :return: the directory as a string
    """
    return __init__.EVENT_DATA


def get_localisation_file():
    """
    Get the directory of the localisation file.

    :postcondition: get the directory of the file
    :return: the directory as a string
    """
    return __init__.LOCALISATION


def get_map_data(identifiers: list[str]) -> dict[str: ...]:
    """
    Get data from the map data file.

    :param identifiers: a list of identifiers for the data
    :precondition: identifiers is a non-empty list of strings corresponding to an entry in map data file
    :precondition: map data file exists as a json
    :postcondition: get the data
    :return: the map data as a dictionary
    """
    with open(get_map_data_file(), 'r') as text_file:
        data = json.load(text_file)
        for name in identifiers:
            data = data[name]
        output = data
    return output


def get_event_data(tile_id: str) -> dict[str: ...]:
    """
    Get data from the event data file.

    :param tile_id: the id of a tile
    :precondition: tile_id corresponds to an entry in the event data file
    :precondition: event data file exists as a json
    :return: the event data as a dictionary
    """
    with open(get_event_data_file(), 'r') as event_data:
        event_json = json.load(event_data)
        event_sequence = event_json["tile_events"][tile_id]
    return event_sequence


def get_localisation() -> dict[str: dict]:
    """
    Get text from the localisation file.

    :precondition: localisation file exists as a json
    :return: the localisation text as a dictionary
    """
    with open(get_localisation_file(), 'r') as text_file:
        localisation = json.load(text_file)
    return localisation
