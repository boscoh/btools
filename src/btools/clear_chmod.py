#!/usr/bin/env python3
import os
import pathlib

__doc__ = "Reclaim for user any files that are not shell scripts"

skip_directories = ["__pycache__", "node_modules", ".git"]


def run(cmd):
    print(cmd)
    os.system(cmd)


def process(d):
    for f in pathlib.Path(d).glob("*"):
        if f.is_dir():
            if f.name in skip_directories:
                continue
            run(f'chmod og-w "{f}"')
            process(f)
        else:
            if not str(f).endswith("sh") and not str(f).endswith("bat"):
                run(f'chmod a-x "{f}"')
            run(f'chmod og-w "{f}"')


def main():
    process(".")


if __name__ == "__main__":
    main()
