"""A clone of the Linux command 'tree'"""
__version__ = '0.0.7'

from pathlib import Path

TEE          = "├──"
ELBOW        = "└──"
PIPE_PREFIX  = "│   "
SPACE_PREFIX = "    "

dir_count, file_count = 0, 0

def color(text) -> str:
    """Returns the object's string in bold blue"""
    return f'\033[94m\033[1m{str(text)}\033[0m'

def print_dir(directory: Path, indent=""):
    # Use the total count of directories and files
    global dir_count, file_count
    # Hide hidden items by default
    items = [item for item in directory.iterdir() if item.name[0] != '.']
    # Alphabetize
    items = sorted(items)
    # Differentiate the last item
    num_of_items = len(items)
    for index, item in enumerate(items):
        last = (index == num_of_items - 1)
        # Print directories recursivly
        if item.is_dir():
            dir_count += 1
            print(f"{indent}{ELBOW if last else TEE} {color(item.name)}")
            print_dir(item, 
             indent= indent + (SPACE_PREFIX if last else PIPE_PREFIX))
        elif item.is_file():
            file_count += 1
            print(f"{indent}{ELBOW if last else TEE} {item.name}")

def report() -> None:
    dir_label = 'directory' if dir_count == 1 else 'directories'
    file_label = 'file' if file_count == 1 else 'files'
    print(f'\n{dir_count} {dir_label}, {file_count} {file_label}')

print(color('.'))
print_dir(Path.cwd())
report()