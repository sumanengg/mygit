# mygit

A minimal version control system implementation inspired by Git, written in Python. This project demonstrates the internal workings of Git-like version control systems.

## Features

### Basic Operations
- `init`: Initializes a new repository in `.mygit`
- `hash-object <file>`: Stores a file as a content-addressed blob object
- `cat-file <oid>`: Prints the content of an object by its OID

### Tree Operations
- `write-tree`: Creates a tree object representing the current directory structure
- `read-tree <tree_oid>`: Restores the directory structure and files from a tree object

### Version Control
- `commit -m "<message>"`: Creates a commit with the current directory state
- `mylog`: Shows commit history starting from HEAD

## Installation

```bash
# Clone the repository
git clone https://github.com/sumanengg/mygit.git
cd mygit

# Install in development mode
pip install -e .
```

## Usage

### Repository Setup
```bash
# Initialize a new repository
mygit init
```

### Working with Objects
```bash
# Store a file in the object database
mygit hash-object myfile.txt

# View object contents
mygit cat-file <object_id>
```

### Managing Directory State
```bash
# Create a tree object from current directory
mygit write-tree

# Restore directory state from a tree
mygit read-tree <tree_id>
```

### Version Control
```bash
# Create a commit
mygit commit -m "Initial commit"

# View commit history
mygit mylog
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
