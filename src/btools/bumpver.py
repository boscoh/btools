#!/usr/bin/env python3

"""Bumpver of pyproject.toml."""

import os
import sys
from pathlib import Path

import semver
from cyclopts import App

app = App(help_flags=["--help", "-h"])


def run_as_shell(txt):
    for line in txt.splitlines():
        if not line.strip():
            continue
        print(f">> {line}")
        os.system(line)


@app.default
def main(action: str = None):
    """Bump version in pyproject.toml and commit changes.

    :param action: Version component to bump (major, minor, or patch)
    """
    if action is None:
        print("Usage: bumpver [major|minor|patch]")
        print("\nBump version in pyproject.toml and commit changes.")
        sys.exit(0)
    curr_dir = Path.cwd()
    pyproject_toml = curr_dir / "pyproject.toml"

    if not pyproject_toml.exists():
        print("Couldn't find pyproject.toml")
        sys.exit()

    lines = pyproject_toml.read_text().splitlines()
    version_str = None
    for line in lines:
        if "version" in line:
            version_str = eval(line.split("=")[-1])
            break

    if not version_str:
        print("Couldn't find version in pyproject.toml")
        sys.exit()

    print("Current version:", version_str)

    action = action.lower()
    version = semver.Version.parse(str(version_str))

    if action == "major":
        new_version = version.bump_major()
    elif action == "minor":
        new_version = version.bump_minor()
    elif action == "patch":
        new_version = version.bump_patch()
    else:
        print(f"Unknown action: {action}")
        sys.exit()

    print("Bumped version:", new_version)

    out_lines = []
    for line in pyproject_toml.read_text().splitlines():
        if "version" in line:
            line = line.replace(version_str, str(new_version))
        out_lines.append(line)

    pyproject_toml.write_text("\n".join(out_lines) + "\n")

    run_as_shell(f"""
    git commit -am "version bump {new_version}"
    git push
    """)


if __name__ == "__main__":
    app()
