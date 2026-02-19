#!/usr/bin/env python3

"""Shared utilities for btools scripts."""

import subprocess
import sys


def run(cmd: str, env=None) -> None:
    """Run a shell command, printing it first. Exits on failure.

    :param cmd: Shell command to run
    :param env: Optional environment variables dict
    """
    print(f">> {cmd}")
    result = subprocess.run(cmd, shell=True, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)


def run_output(cmd: str) -> str:
    """Run a shell command and return its output as text.

    :param cmd: Shell command to run
    :return: stdout+stderr output, or empty string on error
    """
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError:
        return ""
