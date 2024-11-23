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


def main():
    example_text = get_text("intro", "0000")
    print(example_text)


if __name__ == "__main__":
    main()
