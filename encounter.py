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
        print("Your foe challenges you to a guessing game!")
        user_guess = input("Guess a number from 1-5: ")
        try:
            user_guess = int(user_guess)
        except ValueError:
            print("Not a number!")
        else:
            if user_guess == random_number:
                print("\nCorrect! The number was", random_number)
            else:
                print("\nIncorrect! The number was", random_number)
    return guessing_game


def start_encounter(board: dict, character: dict):
    print(get_text("encounter", "start", True))
    encounter = generate_encounter(board, character)
    encounter()


def main():
    start_encounter({}, {})


if __name__ == "__main__":
    main()
