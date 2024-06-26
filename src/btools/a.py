#!/usr/bin/env python3

from __future__ import print_function

import glob
import os
import sys

from path import Path

__doc__ = "Quick open applications in Darwin"

home = str(Path.home()) 
search_dirs = ['/Applications/', f'{home}/MyApps'] 

print(search_dirs) 

def get_name(f):
    base = os.path.basename(f)
    return base.replace('.app', '').lower()

def find_match(apps, use_app): 
    for app in apps: 
        if use_app in app: 
            return app 
        return None 
    
def main():
    if len(sys.argv) < 2:
        print("Open OSX apps (searches for text fit to App name)")
        print("Usage: a app_name param1 param2 ...")
    else:
        params = sys.argv[1:]

        use_app = params[0].lower()
        for search_dir in search_dirs: 
            fnames = glob.glob(os.path.join(search_dir, '*'))
            apps = [get_name(f) for f in fnames]
            if match_app := find_match(apps, use_app): 
                params[0] = match_app 
                break

        params = ['"%s"' % p for p in params]
        cmd = 'open -a ' + ' '.join(params)

        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    main()
