"""The model/veiwer class for the tree"""
__version__ = '0.2.2'

import os, stat
from pathlib import Path
from datetime import datetime, timedelta

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

def color(text, color='blue') -> str:
    """Returns the object's string in bold of the specified color."""
    color_code = {'blue': 94, 'green': 92}[color]
    return f'\033[{color_code}m\033[1m{str(text)}\033[0m'

is_exec = lambda file: os.access(file, os.X_OK)


class Tree():
    """Model and viewer for directory trees.
    
    Saves the settings from the command-line type input, processes 
    the directory data into a tree, and reports the directory count 
    and the file count.

    Keyword Arguments:
        - hide  -- Hide hidden files, whose name begins with "."
        - dirs  -- List directories only
        - inode -- Displays the inode code for the file/directory
        - dev   -- Displays the device code
        - mode  -- Displays the mode code for the file/directory
        - owner -- Displays the file/directory owner
        - group -- Displays the file/directory owner group
        - size  -- Displays the size of the file/directory in bytes
        - units -- Displays the size in kilobytes, megabytes, etc.
        - date  -- Displays the date and time, by default of modification
        - classify -- Appends / to the end of a directory name 
                   and * to an executable
        - chrono -- Sorts the files/directories by modification time
        - sort  -- Alphabetize the files/directories list
        - reverse -- List the directory contents in reverse order
    """
    def __init__(self, 
        hide=True,
        dirs=False,
        inode=False,
        dev=False,
        mode=False,
        owner=False,
        group=False,
        size=False,
        units=False,
        date=False,
        classify=False,
        chrono=False,
        sort=True,
        reverse=False,
    ) -> None:
        self.dir_count, self.file_count = 0, 0
        self.hide = hide
        self.dirs = dirs
        self.inode = inode
        self.dev = dev
        self.mode = mode
        self.owner = owner
        self.group = group
        self.size = size
        self.units = units
        self.date = date
        self.classify = classify
        self.chrono = chrono
        self.sort = sort
        self.reverse = reverse

    def trunk(self, directory: Path) -> None:
        """Checks that the given path is a directory, prints its name 
        in bold blue, and prints the directory tree.
        """
        directory = Path(directory)
        if directory.is_dir():
            print(color(directory))
            self.print_dir(directory)
        else:
            print(directory, "[error opening dir]")

    def _prepare_list(self, directory: Path) -> list:
        """Filters and sorts the list of items in a directory 
        according the the command-line settings.
        """
        # Start with all the items in the directory
        items = [*directory.iterdir()]
        if self.hide:
            # Hide hidden items
            items = [item for item in items if item.name[0] != '.']
        if self.dirs:
            # List directories only
            items = [item for item in items if item.is_dir()]
        if self.chrono:
            items = sorted(items, key=lambda item: item.stat().st_mtime)
        elif self.sort:
            # Alphabetize
            items = sorted(items, key=lambda item: item.name.lower())
        if self.reverse:
            items.reverse()
        return items

    def _item_stats(self, file: Path) -> str:
        stats = []
        item_stat = file.stat()
        if self.inode:
            stats.append(f'{item_stat.st_ino}')
        if self.dev:
            stats.append(f'{item_stat.st_dev:3}')
        if self.mode:
            stats.append(stat.filemode(item_stat.st_mode))
        if self.owner:
            stats.append(file.owner())
        if self.group:
            stats.append(file.group())
        if self.units:
            size = item_stat.st_size
            if   size > 1024**3:
                size = size / 1024**3
                designation = 'G'
            elif size > 1024**2:
                size = size / 1024**2
                designation = 'M'
            elif size > 1024:
                size = size / 1024
                designation = 'K'
            else:
                designation = ''
            if size < 10:
                size = f'{size:.1f}{designation}'
            else:
                size = f'{size:.0f}{designation}'
            stats.append(f'{size:>5}')
        elif self.size:
            stats.append(f'{item_stat.st_size:11}')
        if self.date:
            mtime = datetime.fromtimestamp(item_stat.st_mtime)
            if datetime.now() - mtime < timedelta(days=365):
                stats.append(f"{mtime.strftime('%b')} {mtime.day:>2} "
                             f"{mtime.hour:02}:{mtime.minute:02}")
            else:
                stats.append(f"{mtime.strftime('%b')} {mtime.day:>2} "
                             f"{mtime.year:>5}")
        if stats != []:
            return '[' + ' '.join(stats) + ']  '
        else:
            return ''

    def print_dir(self, directory: Path, indent="") -> None:
        """Prints the tree for a single directory or subdirectory."""
        items = self._prepare_list(directory)
        # Differentiate the last item
        max_index = len(items) - 1
        for index, item in enumerate(items):
            last = (index == max_index)
            stats = self._item_stats(item)
            prefix = f"{indent}{ELBOW if last else TEE} {stats}"
            # Print directories recursivly
            if item.is_dir():
                self.dir_count += 1
                if self.classify:
                    name = item.name + "/"
                else:
                    name = item.name
                print(f"{prefix}{color(name, 'blue')}")
                self.print_dir(item, 
                    indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))
            elif item.is_file():
                self.file_count += 1
                if is_exec(item):
                    if self.classify:
                        name = item.name + "*"
                    else:
                        name = item.name 
                    print(f"{prefix}{color(name, 'green')}")
                else:
                    print(f"{prefix}{item.name}")

    def report(self) -> None:
        """Prints the directory count and the file count."""
        dir_label = 'directory' if self.dir_count == 1 else 'directories'
        file_label = 'file' if self.file_count == 1 else 'files'
        if self.dirs:
            print(f'\n{self.dir_count} {dir_label}')
        else:
            print(f'\n{self.dir_count} {dir_label}, '
                  f'{self.file_count} {file_label}')
