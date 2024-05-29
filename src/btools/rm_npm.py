#!/usr/bin/env python3
from pathlib import Path
import shutil

__doc__ = "Remove node_modules and package-lock.json from directories"

def walk(path): 
    for p in Path(path).iterdir(): 
        yield p.resolve()
        if p.is_dir(): 
            yield from walk(p)

def main():
    p = Path('.').resolve()
    print('Checking for npm modules', p)

    node_modules = []
    package_locks = []
    for d in walk('.'):
        if d.name.endswith('node_modules'):
            node_modules.append(d)
        if d.name.endswith('package-lock.json'):
            package_locks.append(d)

    for f in reversed(package_locks):
        print('remove file', f)
        f.unlink()


    for d in reversed(node_modules):
        print('remove directory', d)
        shutil.rmtree(d)


if __name__ == "__main__":
    main()