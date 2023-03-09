"""A clone of the Linux command 'tree'"""
__version__ = '0.0.1'

from pathlib import Path

TEE          = "├──"

print('.')
for item in Path.cwd().iterdir():
    print(f"{TEE} {item.name}")
print()
