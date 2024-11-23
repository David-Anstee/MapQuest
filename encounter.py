"""
David Anstee
A01434810
"""
import random
from localisation import get_text


def roll_for_encounter(encounter_rate: int = 20) -> bool:
    encounter_roll = random.randint(1, 100)
    return encounter_roll < encounter_rate


def generate_encounter(board: dict, character: dict):
    def guessing_game():
        random_number = random.randint(1, 5)
        user_guess = input("Guess a number from 1-5: ")
        try:
            return int(user_guess) == random_number
        except ValueError:
            print("Not a number!")
            return False
    print(guessing_game)
    return guessing_game


def start_encounter(board: dict, character: dict):
    print(get_text("encounter", "start", True))
    encounter = generate_encounter(board, character)
    encounter()
