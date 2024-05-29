#!/usr/bin/env python3

import numpy
import sys

__doc__ = """Print shape of numpy .npy file"""

def main():
    for arg in sys.argv[1:]:
        m = numpy.load(arg)
        print("Numpy shape", m.shape)



if __name__ == "__main__":
    main()