"""A clone of the Linux command 'tree'"""
__version__ = '0.1.2'

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
        prog=f'python {args[0]}',
        description="A clone of the Linux command 'tree'",
    )
    parser.version = f'tree v{__version__} 2023 by Mordechai Fast'
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "dir_list",
        metavar='<directory list>',
        nargs='*',
        default='.',
    )
    return parser.parse_args(args[1:])

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

def main(args):
    args = parse_args(args)
    for directory in args.dir_list:
        print(directory)
        print_dir(Path(directory))
    print(f'\n{dir_count} directories, {file_count} files')

if __name__ == '__main__':
    main(sys.argv)