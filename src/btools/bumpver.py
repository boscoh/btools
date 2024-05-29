#!/usr/bin/env python3
import sys
import semver
from path import Path
import os

__doc__ = "Bumpver of pyproject.toml. Usage: bump_ver (major|minor|patch)"


def run_as_shell(txt):
    for line in txt.splitlines():
        if not line.strip():
            continue
        print(f">> {line}")
        os.system(line)

def main():
    print(__doc__)
    curr_dir = Path().getcwd()
    pyproject_toml = curr_dir / "pyproject.toml"
    print(f"Looking for {pyproject_toml}")

    if not pyproject_toml.exists():
        print("Couldn't find pyproject.toml")
        sys.exit()

    action = None
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()

    new_version = None
    out_lines = []
    lines = pyproject_toml.lines()
    for line in lines:
        if "version" in line:
            version_str = eval(line.split("=")[-1])
            print("Current version:", version_str)
            version = semver.Version.parse(str(version_str))
            if action == "major":
                new_version = version.bump_major()
            elif action == "minor":
                new_version = version.bump_minor()
            elif action == "patch":
                new_version = version.bump_patch()
            if new_version:
                line = line.replace(version_str, str(new_version))
                print("Bumped version:", new_version)
        out_lines.append(line)

    if new_version:
        pyproject_toml.write_lines(out_lines)

    run_as_shell(f"""
    git commit -am "version bump {new_version}"
    git push
    """)

if __name__ == "__main__":
    main()