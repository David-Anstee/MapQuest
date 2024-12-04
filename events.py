import json
import game
import player_input

EVENT_FILE = "event_data.json"


def get_event_sequence(tile_id: str) -> dict[str: ...]:
    with open(EVENT_FILE, 'r') as event_data:
        event_json = json.load(event_data)
        event_sequence = event_json["tile_events"][tile_id]
        return event_sequence


def get_next_stage(game_state: dict[str: dict], choice: dict[str: ...]) -> str:
    if "skill_check" in choice:
        skill_check_data = choice["skill_check"]
        stat = skill_check_data[0]
        target = skill_check_data[1]
        success = game.skill_check(game_state=game_state, stat=stat, target=target)
    else:
        success = True
    next_stage = choice["success"] if success else choice["failure"]
    return next_stage


def apply_effects(game_state: dict[str: dict], event_stage: dict[str: ...]):
    if "effects" in event_stage:
        effects = event_stage["effects"]
        for effect_target in effects:
            for effect in effects[effect_target].items():
                game_state[effect_target][effect[0]] += effect[1]


def run_event_stage(game_state: dict[str: dict], event_stage: dict[str: ...]) -> str:
    apply_effects(game_state, event_stage)

    description = event_stage["description"]
    option_data = event_stage["options"]
    options = list(option_data.keys())

    user_input = player_input.get_user_input(game_state=game_state, options=options, option_prompt=description,
                                             prompt_namespace="event_desc", option_namespace="event_option")
    choice = option_data[user_input]

    next_stage = get_next_stage(game_state=game_state, choice=choice)
    return next_stage


def start_event(game_state: dict[str: dict], tile_id: str):
    try:
        event_sequence = get_event_sequence(tile_id)
    except FileNotFoundError:
        print(f"MISSING FILE {EVENT_FILE}")
        return
    except KeyError:
        print(f"EVENT NOT FOUND: {tile_id}")
        return

    xp_reward = 0
    event_stage = "0"
    while event_stage != "-1":
        event = event_sequence[event_stage]
        xp_reward += event["xp"] if "xp" in event else 0
        event_stage = run_event_stage(game_state=game_state, event_stage=event)

    if xp_reward:
        game.add_xp(game_state=game_state, amount=xp_reward)


def main():
    pass


if __name__ == "__main__":
    main()
