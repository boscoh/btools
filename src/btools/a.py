#!/usr/bin/env python3

"""Quick open applications in Darwin"""

import glob
import os
from pathlib import Path

from cyclopts import App

app = App()

search_dirs = ["/Applications/", f"{Path.home()}/MyApps"]


def get_name(f):
    base = os.path.basename(f)
    return base.replace(".app", "").lower()


def find_match(apps, use_app):
    for app in apps:
        if use_app in app:
            return app
    return None


@app.default
def main(*params: str):
    """Open macOS applications by partial name match.

    :param params: Application name followed by optional parameters to pass to the app
    """
    if not params:
        print("Open OSX apps (searches for text fit to App name)")
        print("Usage: a app_name param1 param2 ...")
        return

    params = list(params)
    use_app = params[0].lower()
    for search_dir in search_dirs:
        fnames = glob.glob(os.path.join(search_dir, "*"))
        apps = [get_name(f) for f in fnames]
        if match_app := find_match(apps, use_app):
            params[0] = match_app
            break

    params = [f'"{p}"' for p in params]
    cmd = "open -a " + " ".join(params)

    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    app()
