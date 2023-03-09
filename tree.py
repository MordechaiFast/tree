"""A clone of the Linux command 'tree'"""
__version__ = '0.0.3'

from pathlib import Path

TEE          = "├──"
PIPE_PREFIX  = "│   "

def print_dir(directory: Path, indent=""):
    # Hide hidden items by default
    items = [item for item in directory.iterdir() if item.name[0] != '.']
    for item in items:
        print(f"{indent}{TEE} {item.name}")
        if item.is_dir():
            print_dir(item, indent=indent+PIPE_PREFIX)

print('.')
print_dir(Path.cwd())
print()
