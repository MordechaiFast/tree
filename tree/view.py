"""Display functions for the Tree class."""
__version__ = '0.1.0'

from .tree_class import Tree

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

def color(text) -> str:
    """Returns the object's string in bold blue"""
    return f'\033[94m\033[1m{str(text)}\033[0m'

def grafic_print(tree: Tree) -> None:
    """Diplays the directory tree in graphic format on the terminal."""
    for directory in tree.listing:
        if type(directory) is list:
            print(color(directory[0]))
            _print_dir(directory[1:])
        else:
            # The directory does not exist
            print(directory)
        
def _print_dir(directory: list, indent=''):
    # Differentiate the last item
    max_index = len(directory) - 1
    for index, item in enumerate(directory):
        last = (index == max_index)
        if type(item) is list:
            # Print directories recursivly
            print(f"{indent}{ELBOW if last else TEE} {color(item[0])}")
            _print_dir(item[1:], 
                indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))
        else:
            print(f"{indent}{ELBOW if last else TEE} {item}")
