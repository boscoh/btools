#!/usr/bin/env python3

import io
import sys
import textwrap
import typing
from json import load as json_load

import click
from ruyaml import YAML

__doc__ = "Convert json to python dict repr"

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


d = {
    "command": "heat",
    "granary": "3gb1.implicit.parmed",
    "heat": {
        "atom_mask": "protein ligand noh",
        "equil_time_ns": 0.5,
        "n_stage_heat": 5,
        "n_stage_release": 5,
        "stage_time_ns": 0.2,
        "x": {"y": {"z": 1}},
        "t": [1, [3, {"k": "y"}], 2, {"z": {"k": 3}}],
        "start_restraint_weight_kcal_per_mol_per_angstroms2": 2,
        "start_temp_k": 100,
        "target_temp_k": 300,
        "use_barostat_for_equil": False,
        "use_barostat_for_heating": False,
        "use_barostat_for_release": False,
    },
    "output": {"traj_interval_ps": 10, "traj_out": "trajectory.h5"},
    "runner": "rseed.heat.HeatRunner",
    "sim": "Sim",
    "type": "rsjob.runner",
    "version": "1.41+0.g3cb14cf.dirty",
}


@click.command()
@click.option(
    "--json",
    help="incoming json",
)
@click.option(
    "--yaml",
    help="incoming yaml",
)
def run(json, yaml):
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
        print(
            textwrap.dedent(
                """
                to_dict converts json to python dict format
                
                usage: 
                   to_dict --json my.json
                   to_dict --yaml my.yaml
                   cat <json file> | to_dict
                   to_dict < my.json
                   echo '{"key": false}' | to_dict
                """
            )
        )
        sys.exit(0)
    walk_d(incoming_json)
    contents = output.getvalue()
    output.close()
    print(contents)


if __name__ == "__main__":
    run()
