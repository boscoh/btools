#!/usr/bin/env python3
import sys
import semver
from path import Path

__doc__ = "Bump version of pyproject.toml: bump_ver [major|minor|patch]"

def main():
    curr_dir = Path().cwd()
    print(f"Looking for python project in {curr_dir}")
    pyproject_toml = curr_dir / "pyproject.toml"

    if not pyproject_toml.exists():
        print("Couldn't find pyproject.toml")
        sys.exit()

    out_lines = []
    lines = pyproject_toml.lines()
    for line in lines:
        if "version" in line:
            version_str = eval(line.split("=")[-1])
            version = semver.Version.parse(version_str)
            print(version)
        out_lines.append(line)

if __name__ == "__main__":
    main()