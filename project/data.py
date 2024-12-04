import __init__
import json


def get_data_file():
    return __init__.GAME_DATA


def get_data(identifiers: list[str]):
    output = None
    with open(get_data_file(), 'r') as text_file:
        data = json.load(text_file)
        for name in identifiers:
            data = data[name]
        output = data
    return output


def main():
    example_data = get_data(["tiles", "early", "00"])
    print(example_data)


if __name__ == "__main__":
    main()
