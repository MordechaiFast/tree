#! /usr/bin/python
"""A clone of the Linux command 'tree'"""
__version__ = '0.2.0'

import sys
import argparse
from pathlib import Path
from .tree import Tree

def main(args: list):
    """Work with the command-line input and output"""
    args = parse_args(args)
    tree = Tree(
        hide=not args.show,
        dirs=args.dirs,
        sort=not args.unsort
    )
    for directory in args.dir_list:
        tree.root(Path(directory))
    tree.report()

def parse_args(args: list) -> argparse.Namespace:
    """Parse the comand-line arguments."""
    parser = argparse.ArgumentParser(
        #prog=f'python {args[0]}',
        description="A clone of the Linux command 'tree'",
    )
    parser.version = f'tree v{__version__} 2023 by Mordechai Fast'
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "dir_list",
        metavar='<directory list>',
        help="The directories to be listed",
        nargs='*',
        default='.',
    )
    parser.add_argument(
        '-a',
        dest='show',
        action='store_true',
        help="All files are listed.",
    )
    parser.add_argument(
        '-d',
        dest='dirs',
        action='store_true',
        help="List directories only.",
    )
    parser.add_argument(
        '-U',
        dest='unsort',
        action='store_true',
        help="Leave files unsorted.",
    )
    return parser.parse_args(args[1:])

if __name__ == '__main__':
    main(sys.argv)
