"""A clone of the Linux command 'tree'"""
__version__ = '0.0.2'

from pathlib import Path

TEE          = "├──"
PIPE_PREFIX  = "│   "

def print_dir(directory: Path, indent=""):
    for item in directory.iterdir():
        print(f"{indent}{TEE} {item.name}")
        if item.is_dir():
            print_dir(item, indent=indent+PIPE_PREFIX)

print('.')
print_dir(Path.cwd())
print()
