#!/usr/bin/env python3

"""Print shape of numpy .npy file"""

import numpy
from cyclopts import App

app = App()


@app.default
def main(*files: str):
    """Print shape of numpy .npy files.

    :param files: One or more .npy files to read
    """
    for arg in files:
        m = numpy.load(arg)
        print("Numpy shape", m.shape)


if __name__ == "__main__":
    app()
