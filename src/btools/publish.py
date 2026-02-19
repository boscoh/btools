#!/usr/bin/env python3

"""Bump version, commit, push, and publish to PyPI."""

import re
import subprocess
import sys
from pathlib import Path
from typing import Literal

from cyclopts import App

app = App()


def run(cmd: str) -> None:
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


@app.default
def main(part: Literal["major", "minor", "patch"]):
    """Bump version, commit, push, and publish package to PyPI.

    :param part: Version component to bump (major, minor, or patch)
    """
    pyproject = Path("pyproject.toml")
    text = pyproject.read_text()

    match = re.search(r'^version = "(\d+)\.(\d+)\.(\d+)"', text, re.MULTILINE)
    if not match:
        print("Could not find version in pyproject.toml")
        sys.exit(1)

    current_version = match.group(1) + "." + match.group(2) + "." + match.group(3)
    print(f"Current version: {current_version}")

    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    pyproject.write_text(text.replace(match.group(0), f'version = "{new_version}"'))
    print(f"Version bumped to {new_version}")

    run(f'git add pyproject.toml && git commit -m "Bump version to {new_version}"')
    run("git push")
    run("uv build")
    run(f"uv publish dist/*-{new_version}*")


if __name__ == "__main__":
    app()
