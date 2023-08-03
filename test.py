import re
import shlex
from typing import Callable


def parse_command(input_string: str, command_handlers: dict[str, Callable]):
    tokens = shlex.split(input_string)[1:]
    command: str = None
    value: str = None
    flags: list[str] = list()
    arguments: dict[str, str] = dict()

    i = 0
    while i < len((tokens)):
        token = tokens[i]

        if i == 0:
            if re.match('^[a-zA-Z]+$', token):
                command = token.lower()
            else:
                command = 'error'
        elif i == 1 and not token.startswith('-'):
            value = token
        elif token.startswith('--'):
            key, val = token[2:], tokens[i+1]
            if not val.startswith('--'):
                arguments[key] = val
            i += 1
        elif token.startswith('-'):
            flags.append(token[1:])

        i += 1

    args = { 'value': value, 'flags': flags, 'arguments': arguments }
    command_handlers[command](**args)


def download_handler(value: str | None, flags: list[str], arguments: dict[str, str]):
    print(value)
    print(flags)
    print(arguments)

command_handlers = {
    'download': download_handler
}
input_string = 'eagold download va234lue -f -r --arg1 valueforarg1 --arg2 valueforarg2'

parse_command(input_string, command_handlers)