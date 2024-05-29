#!/usr/bin/env python3

from __future__ import print_function
import sys
import os
import glob

__doc__ = "Quick open applications in Darwin"

applications_dir = '/Applications/'


def get_name(f):
    base = os.path.basename(f)
    return base.replace('.app', '').lower()


def main():
    if len(sys.argv) < 2:
        print("Open OSX apps (searches for text fit to App name)")
        print("Usage: a app_name param1 param2 ...")
    else:
        params = sys.argv[1:]

        use_app = params[0].lower()

        apps = glob.glob(os.path.join(applications_dir, '*'))
        apps = [get_name(a) for a in apps]

        for app in apps:
            if use_app in app:
                params[0] = app

        params = ['"%s"' % p for p in params]
        cmd = 'open -a ' + ' '.join(params)

        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    main()