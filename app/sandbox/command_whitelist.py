import re


ALLOWED_COMMANDS = [
    r"python.*\.py",
    r"pytest.*",
    r"npm test",
    r"cargo test",
    r"make test",
]


def is_command_allowed(command: str) -> bool:
    return any(re.match(pattern, command) for pattern in ALLOWED_COMMANDS)
