#!/usr/bin/env python3

"""Convert json to python dict repr"""

import io
import sys
import typing
from json import load as json_load

from cyclopts import App
from ruyaml import YAML

app = App()

indent = "  "

output = io.StringIO()


def print_out(*args, **kwargs):
    print(*args, file=output, **kwargs)


def walk_d(o, level=0, skip_first_indent=False):
    curr_space = indent * level
    if not skip_first_indent:
        print_out(curr_space, end="")
    if isinstance(o, typing.Mapping):
        print_out("dict(")
        next_space = "  " * (level + 1)
        for i, (key, value) in enumerate(o.items()):
            print_out(next_space, end="")
            print_out(f"{key}=", end="")
            if isinstance(value, typing.Mapping):
                walk_d(value, level + 1, True)
            else:
                walk_d(value, level + 1, True)
        print_out(curr_space, end="")
        if level > 0:
            print_out("),", end="")
        else:
            print_out(")", end="")
        print_out()
    elif isinstance(o, typing.List):
        print_out("[", end="")
        print_out()
        for item in o:
            walk_d(item, level + 1)
        print_out(curr_space, end="")
        print_out("],", end="")
        print_out()
    elif isinstance(o, str):
        print_out(f'"{o}",', end="")
        print_out()
    else:
        print_out(f"{o},", end="")
        print_out()



@app.default
def run(json: str = None, yaml: str = None):
    """Convert JSON or YAML to Python dict format.

    Reads from stdin if no file is specified.

    :param json: Path to incoming JSON file
    :param yaml: Path to incoming YAML file
    """
    if json:
        with open(json) as f:
            incoming_json = json_load(f)
    elif yaml:
        yaml_reader = YAML(typ="safe")
        yaml_reader.default_flow_style = False
        with open(yaml) as handle:
            incoming_json = yaml_reader.load(handle)
    elif not sys.stdin.isatty():
        incoming_json = json_load(sys.stdin)
    else:
        app.help_print()
        return
    walk_d(incoming_json)
    contents = output.getvalue()
    output.close()
    print(contents)


if __name__ == "__main__":
    app()
