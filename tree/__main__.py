#! /usr/bin/python
"""A clone of the Linux command 'tree'"""
__version__ = '0.2.2'

import sys
import argparse
from .tree import Tree

def main(args: list):
    """Work with the command-line input and output"""
    args = parse_args(args)
    tree = Tree(
        hide=not args.all,
        dirs=args.dirs,
        inode=args.inodes,
        dev=args.device,
        mode=args.protections,
        owner=args.UID,
        group=args.GID,
        size=args.size,
        units=args.human,
        date=args.date,
        classify=args.classify,
        chrono=args.time,
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
        add_help=False,
    )
    parser.version = f'tree v{__version__} 2023 by Mordechai Fast'
    parser.add_argument(
        dest="dir_list",
        metavar='<directory list>',
        #help="The directories to be listed",
        nargs='*',
        default='.',
    )
    listing = parser.add_argument_group("Listing options")
    listing.add_argument(
        '-a',
        dest='all',
        action='store_true',
        help="All files are listed.",
    )
    listing.add_argument(
        '-d',
        dest='dirs',
        action='store_true',
        help="List directories only.",
    )
    listing.add_argument(
        '--noreport',
        action='store_true',
        help='Turn off file/directory count at end of tree listing.',
    )
    file = parser.add_argument_group("File options")
    file.add_argument(
        '-p',
        dest='protections',
        action='store_true',
        help='Print the protections for each file.',
    )
    file.add_argument(
        '-u',
        dest='UID',
        action='store_true',
        help='Displays file owner or UID number.',
    )
    file.add_argument(
        '-g',
        dest='GID',
        action='store_true',
        help='Displays file group owner or GID number.',
    )
    file.add_argument(
        '-s',
        dest='size',
        action='store_true',
        help='Print the size in bytes of each file.'
    )
    file.add_argument(
        '-h',
        dest='human',
        action='store_true',
        help='Print the size in a more human readable way.',
    )
    file.add_argument(
        '-D',
        dest='date',
        action='store_true',
        help='Print the date of last modification.',
    )
    file.add_argument(
        '-F',
        dest='classify',
        action='store_true',
        help="Appends '/' or '*' as per ls -F."
    )
    file.add_argument(
        '--inodes',
        action='store_true',
        help='Print inode number of each file.',
    )
    file.add_argument(
        '--device',
        action='store_true',
        help='Print device ID number to which each file belongs.'
    )
    sort = parser.add_argument_group("Sorting options")
    sort.add_argument(
        '-t',
        dest='time',
        action='store_true',
        help='Sort files by last modification time.',
    )
    sort.add_argument(
        '-U',
        dest='unsort',
        action='store_true',
        help="Leave files unsorted.",
    )
    sort.add_argument(
        '-r',
        dest='reverse',
        action='store_true',
        help='Reverse the order of the sort.',
    )
    misc = parser.add_argument_group("Miscellaneous options")
    misc.add_argument("-v", "--version", action="version")
    misc.add_argument(
        '--help',
        action='help',
        help='show this help message and exit'
    )
    return parser.parse_args(args[1:])

if __name__ == '__main__':
    main(sys.argv)
