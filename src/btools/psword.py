#!/usr/bin/env python3

"""Find processes with name"""

import subprocess

from cyclopts import App

app = App()


def run(cmd):
    try:
        bytes_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        text = bytes_output.decode("utf-8", errors="ignore")
        return text
    except subprocess.CalledProcessError:
        return ""


@app.default
def main(*words: str, kill: bool = False):
    """Find processes by name and optionally kill them.

    :param words: Process names to search for
    :param kill: If True, kill matching processes
    """
    if not words:
        print("Usage: psword [-k] <word>")
        return

    for word in words:
        txt = run(f"ps aux | grep {word}")
        for line in txt.splitlines():
            tokens = line.split()
            i_process = tokens[1]
            cmd = " ".join(tokens[10:])
            if len(cmd) > 80:
                cmd = cmd[:80] + "..."
            if "psword" in line:
                continue
            if kill:
                kill_cmd = f"kill -9 {i_process}"
                print(f"cmd: {kill_cmd} ({cmd})")
                run(kill_cmd)
            else:
                print(f"process {i_process}: {cmd}")


if __name__ == "__main__":
    app()
