#!/usr/bin/env python3

import subprocess
import sys

def run(cmd):
    try:
        bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        text = bytes.decode("utf-8", errors="ignore")
        return text
    except subprocess.CalledProcessError:
        return ""



__doc__ = """
Find processes with name

Usage: psword [-k] <word>

Print simple parquet files as images

Options:
-k   kill jobs
"""


def main():
    args = sys.argv[1:]

    is_kill = '-k' in args
    if is_kill:
        args.remove('-k')

    if not len(args):
        print(__doc__)
        sys.exit(1)


    for word in args:
        txt = run(f"ps aux | grep {word}")
        for line in txt.splitlines():
            tokens = line.split()
            id = tokens[1]
            cmd = " ".join(tokens[10:])
            if len(cmd) > 80:
                cmd = cmd[:80] + "..."
            if 'psword' in line:
                continue
            if is_kill:
                kill_cmd = f"kill -9 {id}"
                print(f"cmd: {kill_cmd} ({cmd})")
                run(kill_cmd)
            else:
                print(f"process {id}: {cmd}")




if __name__ == "__main__":
    main()