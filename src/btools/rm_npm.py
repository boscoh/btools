#!/usr/bin/env python3

"""Remove node_modules and package-lock.json from directories"""

import shutil
from pathlib import Path

from cyclopts import App

app = App()


def walk(path):
    for p in Path(path).iterdir():
        yield p.resolve()
        if p.is_dir():
            yield from walk(p)


@app.default
def main():
    """Recursively remove node_modules directories and package-lock.json files."""
    p = Path(".").resolve()
    print("Checking for npm modules", p)

    node_modules = []
    package_locks = []
    for d in walk("."):
        if d.name.endswith("node_modules"):
            node_modules.append(d)
        if d.name.endswith("package-lock.json"):
            package_locks.append(d)

    for f in reversed(package_locks):
        print("remove file", f)
        f.unlink()

    for d in reversed(node_modules):
        print("remove directory", d)
        shutil.rmtree(d)


if __name__ == "__main__":
    app()
