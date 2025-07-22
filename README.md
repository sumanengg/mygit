# mygit

A minimal version control CLI tool inspired by Git, written in Python.

## Features

- `init` command: Initializes a new repository in `.mygit`.
- `hash-object <file>`: Stores a file as a content-addressed blob object.
- `cat-file <oid>`: Prints the content of an object by its OID.
- `write-tree`: Creates a tree object representing the current directory structure and prints its OID.
- `read-tree <tree_oid>`: Restores the directory structure and files from a tree object.

## Installation

From the project root, install in editable mode:
```bash
pip install -e .
```

## Usage

Initialize a repository:
```bash
mygit init
```

Store a file as a blob object:
```bash
mygit hash-object cats.txt
```

Print the content of an object:
```bash
mygit cat-file <oid>
```

Create a tree object for the current directory:
```bash
mygit write-tree
```

Restore files and directories from a tree object:
```bash
mygit read-tree <tree_oid>
```

## Project Structure

```
mygit/
    cli.py
    base.py
    data.py
setup.py
README.md
```

## Requirements

- Python 3.7+

## Notes
- Objects are stored in `.mygit/objects`.
- Tree objects represent directory structure and reference blobs/trees by their OIDs.
- Hidden files and `.mygit` are ignored when creating tree objects.
