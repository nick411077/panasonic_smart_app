def model_type_aliases(model_type: str | None) -> list[str]:
    if not model_type:
        return []

    aliases = [model_type]
    if model_type.endswith("FA"):
        aliases.append(model_type[:-2])

    return list(dict.fromkeys(aliases))


def model_types_match(model_type: str | None, target_model_type: str | None) -> bool:
    return (
        model_type in model_type_aliases(target_model_type)
        or target_model_type in model_type_aliases(model_type)
    )


def command_has_list(command: dict) -> bool:
    try:
        command_list = command["JSON"][0]["list"]
    except (KeyError, IndexError, TypeError):
        return False

    return isinstance(command_list, list) and len(command_list) > 0


def find_model_commands(command_list: list, model_type: str | None) -> list:
    commands = []
    for alias in model_type_aliases(model_type):
        commands.extend(
            filter(
                lambda c: c.get("ModelType") == alias and command_has_list(c),
                command_list,
            )
        )

    return commands
