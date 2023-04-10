# coding: utf-8
from pathlib import Path
import os, sys

green = lambda name: f'\033[01;32m{name}\033[0m'
blue = lambda name: f'\033[01;34m{name}\033[0m'
is_exec = lambda file: os.access(file, os.X_OK)

def print_dir(directory, prefix='', output=sys.stdout):
    dir_name = f"{prefix}{directory.name or '.'}"
    print(blue(dir_name), file=output)
    for item in directory.iterdir():
        if item.name[0]!='.':
            if item.is_dir():
                print_dir(item, dir_name+"/", output=output)
            else:
                if is_exec(item):
                    print(green(f"{dir_name}/{item.name}"), file=output)
                else:
                    print(f"{dir_name}/{item.name}", file=output)
                
if __name__ == '__main__':
    with open('fullout', mode='w') as file:
        print_dir(Path("."), output=file)