"""The model/veiwer class for the tree"""

from pathlib import Path

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

def color(text) -> str:
    """Returns the object's string in bold blue"""
    return f'\033[94m\033[1m{str(text)}\033[0m'

class Tree():
    """Model and viewer for directory trees.
    
    Saves the settings from the command-line type input, processes 
    the directory data into a tree, and reports the directory count 
    and the file count.

    Keyword Arguments:
        - hide -- Hide hidden files, whose name begins with "."
        - dirs -- List directories only
        - sort -- Alphabetize the files/directories list
    """
    def __init__(self, hide=True, dirs=False, sort=True) -> None:
        # Use the total count of directories and files
        self.dir_count, self.file_count = 0, 0
        self.hide = hide
        self.dirs = dirs
        self.sort = sort

    def root(self, directory: Path) -> None:
        """Checks that the given path is a directory, prints its name 
        in bold blue, and prints the directory tree.
        """
        if directory.is_dir():
            print(color(directory))
            self.print_dir(directory)
        else:
            print(directory, "[error opening dir]")

    def prepare_list(self, directory: Path) -> list:
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
        if self.sort:
            # Alphabetize
            items = sorted(items)
        return items

    def print_dir(self, directory: Path, indent="") -> None:
        """Prints the tree for a single directory or subdirectory."""
        items = self.prepare_list(directory)
        # Differentiate the last item
        max_index = len(items) - 1
        for index, item in enumerate(items):
            last = (index == max_index)
            # Print directories recursivly
            if item.is_dir():
                self.dir_count += 1
                print(f"{indent}{ELBOW if last else TEE} {color(item.name)}")
                self.print_dir(item, 
                    indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))
            elif item.is_file():
                self.file_count += 1
                print(f"{indent}{ELBOW if last else TEE} {item.name}")

    def report(self) -> None:
        """Prints the directory count and the file count."""
        dir_label = 'directory' if self.dir_count == 1 else 'directories'
        file_label = 'file' if self.file_count == 1 else 'files'
        if self.dirs:
            print(f'\n{self.dir_count} {dir_label}')
        else:
            print(f'\n{self.dir_count} {dir_label}, '
                  f'{self.file_count} {file_label}')
