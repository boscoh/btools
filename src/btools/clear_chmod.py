#!/usr/bin/env python3

"""Reclaim for user any files that are not shell scripts"""

from pathlib import Path

from cyclopts import App

from btools.utils import run

app = App()

skip_directories = ["__pycache__", "node_modules", ".git"]


@app.default
def main():
    """Remove execute permissions from non-script files and write permissions from group/other."""
    for f in Path(".").glob("*"):
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


if __name__ == "__main__":
    app()
