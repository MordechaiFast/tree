"""The model class for the tree"""
__version__ = '0.3.0'

from pathlib import Path

class Tree():
    """Model for directory trees.
    
    Saves the settings from the command-line type input, processes 
    the directory data into a tree, and reports the directory count 
    and the file count.

    Keyword Arguments:
        - hide -- Hide hidden files, whose name begins with "."
        - dirs -- List directories only
        - sort -- Alphabetize the files/directories list
    """
    def __init__(self, hide=True, dirs=False, sort=True) -> None:
        # The tree itself
        self.listing = []
        # Use the total count of directories and files
        self.dir_count, self.file_count = 0, 0
        # Save comand-line preferences
        self.hide = hide
        self.dirs = dirs
        self.sort = sort

    def trunk(self, directory: Path) -> None:
        """Checks that the given path is a directory, and adds its 
        contents to the directory tree.
        """
        directory = Path(directory)
        if directory.is_dir():
            self.listing.append(self._branch(directory))
        else:
            self.listing.append(f'{directory} [error opening dir]')

    def _branch(self, directory: Path) -> list:
        """Prints the tree for a single directory or subdirectory."""
        branch_list = [directory.name or '.']
        contents = self._prepare_list(directory)
        for item in contents:
            if item.is_dir():
                self.dir_count += 1
                branch_list.append(self._branch(item))
            elif item.is_file():
                self.file_count += 1
                branch_list.append(item.name)
        return branch_list

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
        if self.sort:
            # Alphabetize
            items = sorted(items, key=lambda item: item.name.lower())
        return items

    def report(self) -> None:
        """Puts the directory count and the file count at the end of 
        the tree.
        """
        dir_label = 'directory' if self.dir_count == 1 else 'directories'
        file_label = 'file' if self.file_count == 1 else 'files'
        if self.dirs:
            self.listing.append(f'\n{self.dir_count} {dir_label}')
        else:
            self.listing.append(f'\n{self.dir_count} {dir_label}, '
                  f'{self.file_count} {file_label}')
