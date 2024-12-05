from project import player_input, tile, state, localisation
from project.localisation import no_supplies_text


def get_options(game_state):
    world = game_state["world"]

    can_travel = "travel" if world["time"] < 6 else "travel_disabled"
    options = [can_travel, "camp", "reflect"]
    return options


def handle_input(game_state: dict[str: dict]):
    options = get_options(game_state)
    user_input = player_input.get_user_input(options=options)

    return do_action(game_state=game_state, user_input=user_input)


def do_action(game_state: dict[str: dict], user_input: str) -> bool:
    input_to_action = {"travel": start_travelling, "camp": start_camping, "reflect": reflect}
    try:
        action = input_to_action[user_input]
    except KeyError:
        print(f"Invalid action!")
        return False

    return action(game_state)


def pass_day(game_state: dict[str: dict]):
    character = game_state["character"]
    if character["supplies"] > 1:
        character["hp"] += 2
        character["supplies"] -= 1
        print(localisation.get_consume_supplies_text(game_state=game_state))
    else:
        print(no_supplies_text(game_state=game_state))
        character["health"] -= 1


def start_camping(game_state: dict[str: dict]):
    options = ["next_day", "cancel"]
    user_input = player_input.get_user_input(options=options)

    if user_input != "cancel":
        camp(game_state=game_state)

        player_input.get_user_input(["continue"])
        return True

    else:
        return False


def camp(game_state: dict[str: dict]):
    character = game_state["character"]

    state.set_time(game_state=game_state, new_time=0)
    pass_day(game_state=game_state)

    character['hp'] = min(character['hp'], character['max_hp'])


def start_travelling(game_state: dict[str, dict]):
    movement = player_input.get_movement()
    if movement != 'cancel':
        direction = player_input.direction_from_input(movement)
        if player_input.move_is_valid(game_state=game_state, direction=direction):
            travel(game_state=game_state, direction=direction)
            return True
        else:
            print("cannot move there")
            return False
    else:
        return False


def travel(game_state: dict[str: dict], direction: list[int, int]):
    character = game_state["character"]

    start_coord = (character["x_coord"], character["y_coord"])
    end_coord = (character["x_coord"] + direction[0], character["y_coord"] + direction[1])

    travel_time = tile.calculate_travel_time(game_state=game_state, start_coord=start_coord, end_coord=end_coord)
    state.pass_time(game_state=game_state, time_passed=travel_time)
    player_input.move_character(game_state=game_state, direction=direction)

    terrain = game_state["board"][end_coord]["terrain"]
    print(f"You arrive in {localisation.get_text("location", terrain)}")


def reflect(game_state: dict[str: dict]):
    reflection_text = localisation.get_reflection_text(game_state=game_state)
    localisation.display_divider()
    print(reflection_text)
    localisation.display_divider()
    player_input.get_user_input(options=["continue"])
