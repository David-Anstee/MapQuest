"""
David Anstee
A01434810
"""
import json

LOCALISATION_FILE = "localisation.json"

def get_text(namespace: str, loc_id: str) -> str:
    try:
        with open(LOCALISATION_FILE, 'r') as text_file:
            localisation = json.load(text_file)
            return localisation[namespace][loc_id]
    except FileNotFoundError:
        return "MISSING LOCALISATION FILE"
    except KeyError:
        return "LOCALISATION NOT FOUND"

