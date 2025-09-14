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

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sumanengg/mygit.git
   cd mygit
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies and the package:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Verify the installation:
   ```bash
   pytest
   ```

### Development Tools

This project uses several development tools:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking
- Pre-commit hooks for automated checks

To run the tools:
```bash
# Format code
black .

# Run linting
flake8 .

# Run type checking
mypy .

# Install pre-commit hooks
pre-commit install

# Run pre-commit hooks on all files
pre-commit run --all-files
```

### Testing

The project uses Python's built-in unittest framework. You can run tests using any of these commands:

```bash
# Using unittest discover (recommended)
python -m unittest discover -v

# Using unittest with specific test file
python -m unittest test.test_mygit -v

# Using pytest (alternative test runner)
pytest test/test_mygit.py -v
```

The test suite includes:
- Repository initialization tests
- Object hashing and storage tests
- Tree operations tests
- Commit functionality tests

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
    __init__.py     # Package initialization
    cli.py          # Command-line interface
    base.py         # Core version control operations
    data.py         # Data storage and object handling
test/
    test_mygit.py   # Test suite
setup.py           # Package configuration
.pre-commit-config.yaml  # Pre-commit hook configuration
README.md         # Project documentation
```

## Requirements

- Python 3.7+

## Notes
- Objects are stored in `.mygit/objects`.
- Tree objects represent directory structure and reference blobs/trees by their OIDs.
- Hidden files and `.mygit` are ignored when creating tree objects.
