"""
David Anstee
A01434810
"""
import random


def roll_for_encounter(encounter_rate: int = 20) -> bool:
    encounter_roll = random.randint(1, 100)
    return encounter_roll < encounter_rate
