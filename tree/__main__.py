#! /usr/bin/python
"""A clone of the Linux command 'tree'"""
__version__ = '0.2.1'

import sys
import argparse
from .tree import Tree

def main(args: list):
    """Work with the command-line input and output"""
    args = parse_args(args)
    tree = Tree(
        hide=not args.show,
        dirs=args.dirs,
        mode=args.protections,
        size=args.size,
        sort=not args.unsort,
        reverse=args.reverse,
    )
    for directory in args.dir_list:
        tree.trunk(directory)
    if not args.noreport:
        tree.report()

def parse_args(args: list) -> argparse.Namespace:
    """Parse the comand-line arguments."""
    parser = argparse.ArgumentParser(
        prog=f'python -m tree',
        description="A clone of the Linux command 'tree'",
    )
    parser.version = f'tree v{__version__} 2023 by Mordechai Fast'
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        dest="dir_list",
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
        '-p',
        dest='protections',
        action='store_true',
        help='Print the protections for each file.',
    )
    parser.add_argument(
        '-s',
        dest='size',
        action='store_true',
        help='Print the size in bytes of each file.'
    )
    parser.add_argument(
        '-U',
        dest='unsort',
        action='store_true',
        help="Leave files unsorted.",
    )
    parser.add_argument(
        '-r',
        dest='reverse',
        action='store_true',
        help='Reverse the order of the sort.',
    )
    parser.add_argument(
        '--noreport',
        action='store_true',
        help='Turn off file/directory count at end of tree listing.'
    )
    return parser.parse_args(args[1:])

if __name__ == '__main__':
    main(sys.argv)
