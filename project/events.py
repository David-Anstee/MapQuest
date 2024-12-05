from project import player_input, state
from project.data import get_event_data
import random

from project.state import should_quit


def skill_check(game_state: dict, target: int, stat=None) -> bool:
    """
    Make a skill check.

    :param game_state: the current game state
    :param target: the target for the skill check
    :param stat: the stat to be added to the skill check
    :precondition: game state is a well-formed dictionary
    :postcondition: make the skill check
    :return: whether the check was successful, as a bool
    """
    character = game_state["character"]
    stat_modifier = 0 if (stat is None) else character[stat]
    difficulty_modifier = 1 if (game_state["world"]["difficulty"] == "easy") else 0
    print("Rolling dice...")

    first_roll = random.randint(1, 6) + difficulty_modifier
    print(first_roll)

    second_roll = random.randint(1, 6) + difficulty_modifier
    print(second_roll)

    print(f"Rolled {first_roll} + {second_roll} = {first_roll+second_roll}.")
    total_roll = first_roll + second_roll + stat_modifier

    if stat_modifier != 0:
        print(f"Modifier ({stat.title()}): {stat_modifier}")
    print(f"Total roll: {total_roll}")

    return total_roll >= target


def get_next_stage(game_state: dict[str: dict], choice: dict[str: ...]) -> str:
    """
    Get the next stage in an event sequence.

    :param game_state: the current game state
    :param choice: the choice selected by the player
    :precondition: game state is a well-formed dictionary
    :precondition: choice is a well-formed dictionary
    :postcondition: get the next event stage
    :return: the next event stage as a string
    """
    if "skill_check" in choice:
        skill_check_data = choice["skill_check"]
        stat = skill_check_data[0]
        target = skill_check_data[1]
        success = skill_check(game_state=game_state, stat=stat, target=target)
    else:
        success = True
    next_stage = choice["success"] if success else choice["failure"]
    return next_stage


def apply_effects(game_state: dict[str: dict], event_stage: dict[str: ...]):
    """
    Apply effects from an event stage.

    :param game_state: the current game state
    :param event_stage: the event stage
    :precondition: game state is a well-formed dictionary
    :precondition: event_stage is a well-formed dictionary
    :postcondition: apply the effects
    """
    if "effects" in event_stage:
        effects = event_stage["effects"]
        for effect_target in effects:
            for effect in effects[effect_target].items():
                game_state[effect_target][effect[0]] += effect[1]


def run_event_stage(game_state: dict[str: dict], event_stage: dict[str: ...]) -> str:
    """
    Run an event stage.

    :param game_state: the current game state
    :param event_stage: the event stage
    :precondition: game state is a well-formed dictionary
    :precondition: event_stage is a well-formed dictionary
    :postcondition: run the event stage
    :return: the next event stage
    """
    apply_effects(game_state, event_stage)

    description = event_stage["description"]
    option_data = event_stage["options"]
    options = list(option_data.keys())

    user_input = player_input.get_user_input(options=options, option_prompt=description,
                                             prompt_namespace="event_desc", option_namespace="event_option")
    choice = option_data[user_input]

    next_stage = get_next_stage(game_state=game_state, choice=choice)
    return next_stage


def start_event(game_state: dict[str: dict], tile_id: str):
    """
    Start an event sequence if one exists.

    :param game_state: the current game state
    :param tile_id: the id of a tile
    :precondition: game state is a well-formed dictionary
    :precondition: tile_id is a string
    :postcondition: run the event sequence for the tile if one exists
    """
    try:
        event_sequence = get_event_data(tile_id)
    except FileNotFoundError:
        print(f"MISSING EVENT FILE")
        return
    except KeyError:
        return

    xp_reward = 0
    time_passed = 0
    event_stage = "0"
    while event_stage != "-1" and not should_quit(game_state=game_state):
        event = event_sequence[event_stage]
        xp_reward += event["xp"] if "xp" in event else 0
        time_passed += event["time"] if "time" in event else 0
        event_stage = run_event_stage(game_state=game_state, event_stage=event)

    if xp_reward:
        state.add_xp(game_state=game_state, amount=xp_reward)
    if time_passed:
        state.pass_time(game_state=game_state, time_passed=time_passed)
