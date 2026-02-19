#!/usr/bin/env python3

"""Quick open applications in Darwin"""

import glob
import os
from pathlib import Path

from cyclopts import App

app = App()

search_dirs = ["/Applications/", f"{Path.home()}/MyApps"]


@app.default
def main(*params: str):
    """Open macOS applications by partial name match.

    :param params: Application name followed by optional parameters to pass to the app
    """
    if not params:
        app.help_print()
        return

    params = list(params)
    use_app = params[0].lower()
    for search_dir in search_dirs:
        names = [Path(f).stem.lower() for f in glob.glob(os.path.join(search_dir, "*"))]
        if match_app := next((name for name in names if use_app in name), None):
            params[0] = match_app
            break

    params = [f'"{p}"' for p in params]
    cmd = "open -a " + " ".join(params)

    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    app()
