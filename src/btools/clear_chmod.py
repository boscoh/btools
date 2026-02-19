#!/usr/bin/env python3

"""Reclaim for user any files that are not shell scripts"""

import os
from pathlib import Path

from cyclopts import App

app = App()

skip_directories = ["__pycache__", "node_modules", ".git"]


def run(cmd):
    print(cmd)
    os.system(cmd)


def process(d):
    for f in Path(d).glob("*"):
        if f.is_dir():
            if f.name in skip_directories:
                continue
            if f.name.startswith("."):
                continue
            run(f'chmod og-w "{f}"')
        else:
            if not str(f).endswith("sh") and not str(f).endswith("bat"):
                run(f'chmod a-x "{f}"')
            run(f'chmod og-w "{f}"')


@app.default
def main():
    """Remove execute permissions from non-script files and write permissions from group/other."""
    process(".")


if __name__ == "__main__":
    app()
