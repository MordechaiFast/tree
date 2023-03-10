"""A clone of the Linux command 'tree'"""
__version__ = '0.1.0'

import sys
import argparse
from pathlib import Path

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

dir_count, file_count = 0, 0

def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='tree',
        description="A clone of the Linux command 'tree'",
    )
    parser.version = 'tree v' + __version__
    parser.add_argument("-v", "--version", action="version")
    return parser.parse_args(args)

def print_dir(directory: Path, indent=""):
    # Use the total count of directories and files
    global dir_count, file_count
    # Hide hidden items by default
    items = [item for item in directory.iterdir() if item.name[0] != '.']
    # Alphabetize
    items = sorted(items)
    # Differentiate the last item
    num_of_items = len(items)
    for index, item in enumerate(items):
        last = (index == num_of_items - 1)
        print(f"{indent}{ELBOW if last else TEE} {item.name}")
        # Print directories recursivly
        if item.is_dir():
            dir_count += 1
            print_dir(item, 
             indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))
        elif item.is_file():
            file_count += 1

parse_args(sys.argv[1:])
print('.')
print_dir(Path.cwd())
print(f'\n{dir_count} directories, {file_count} files')
