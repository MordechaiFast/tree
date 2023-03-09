"""A clone of the Linux command 'tree'"""
__version__ = '0.0.3'

from pathlib import Path

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

def print_dir(directory: Path, indent=""):
    # Hide hidden items by default
    items = [item for item in directory.iterdir() if item.name[0] != '.']
    num_of_items = len(items)
    for index, item in enumerate(items):
        last = (index == num_of_items - 1)
        print(f"{indent}{ELBOW if last else TEE} {item.name}")
        if item.is_dir():
            print_dir(item, 
             indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))

print('.')
print_dir(Path.cwd())
print()
