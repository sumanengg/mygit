from . import data
import os
from collections import namedtuple

# Create the main function for write-tree commands.

def write_tree (directory='.'):
    """Create a tree object from the current directory state.
    
    Args:
        directory (str): Path to the directory to create tree from (default: '.')
    
    Returns:
        str: Object ID of the created tree
    
    Creates a tree object representing the directory structure, recursively
    handling subdirectories and ignoring specified files/directories.
    """
    entries = []
    with os.scandir (directory) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue
            full = f'{directory}/{entry.name}'
            if entry.is_file (follow_symlinks=False):
                type_ = 'blob'
                with open (full, 'rb') as f:
                     oid = data.hash_object (f.read ())
            elif entry.is_dir (follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree (full)
            else:
                continue
            entries.append ((entry.name, oid, type_))

    # TODO actually create the tree object
    tree = ''.join (f'{type_} {oid} {name}\n'
                    for name, oid, type_
                    in sorted (entries))
    return data.hash_object (tree.encode (), 'tree')

def _iter_tree_entries (oid):
    """Internal function to iterate through entries in a tree object.
    
    Args:
        oid (str): Object ID of the tree
    
    Yields:
        tuple: (type, oid, name) for each entry in the tree
    """
    if not oid:
        return
    tree = data.get_object (oid, 'tree')
    for entry in tree.decode ().splitlines ():
        type_, oid, name = entry.split (' ', 2)
        yield type_, oid, name


def get_tree (oid, base_path=''):
    result = {}
    for type_, oid, name in _iter_tree_entries (oid):
        assert '/' not in name
        assert name not in ('..', '.')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update (get_tree (oid, f'{path}/'))
        else:
            assert False, f'Unknown tree entry {type_}'
    return result


def _empty_current_directory():
    """Get a dictionary mapping paths to object IDs from a tree.
    
    Args:
        oid (str): Object ID of the tree
        base_path (str): Base path to prepend to all entries
    
    Returns:
        dict: Mapping of paths to their object IDs
        
    Recursively processes tree objects to build a complete path mapping.
    """
    for path, dirs, filenames in os.walk(".", topdown=False):
        for filename in filenames:
            filepath = os.path.relpath(f'{path}/{filename}')
            if is_ignored(filepath) or not os.path.isfile(filepath):
                continue
            os.remove(filepath)
        for dir in dirs:
            dirpath = os.path.relpath(f'{path}/{dir}')
            if is_ignored(dirpath):
                continue
            try:
                os.rmdir(dirpath)
            except (FileNotFoundError, OSError):
                pass

def read_tree (tree_oid):
    """Restore the working directory to match a tree object.
    
    Args:
        tree_oid (str): Object ID of the tree to restore
    
    Clears the current directory and restores all files and directories
    from the specified tree object.
    """
    _empty_current_directory()
    for path, oid in get_tree (tree_oid, base_path='./').items ():
        os.makedirs (os.path.dirname (path), exist_ok=True)
        with open (path, 'wb') as f:
            f.write (data.get_object (oid))

# Create the main commit message function 

def commit(message):
    """Create a new commit object.
    
    Args:
        message (str): The commit message
    
    Returns:
        str: Object ID of the new commit
    
    Creates a commit object with:
    - Current directory state as tree
    - Current HEAD as parent (if exists)
    - Given commit message
    Updates HEAD to point to the new commit.
    """
    commit = f'tree {write_tree()}\n'
    HEAD = data.get_HEAD()
    if HEAD:
        commit += f"parent {HEAD}\n"
    commit += '\n'
    commit += f'{message}\n'
    oid = data.hash_object(commit.encode(), 'commit')
    data.set_HEAD(oid=oid)


    return oid

LogEntry = namedtuple('LogEntry', ['tree', 'parent', 'message'])
# Log Function to Get Log.
def get_log(oid):
    """Extract information from a commit object.
    
    Args:
        oid (str): Object ID of the commit
    
    Returns:
        LogEntry: Named tuple containing:
            - tree: Object ID of the tree
            - parent: Object ID of parent commit (if any)
            - message: Commit message
    """
    commit_hash_data = data.get_object(oid)
    lines = commit_hash_data.decode().splitlines()
    parent = ''
    tree = ''
    message = []

    while lines:
        line = lines.pop(0)
        if not line:
            break
        key, value = line.split(' ', 1)
        if key == 'tree':
            tree = value
        elif key == 'parent':
            parent = value
        
    message = '\n'.join(lines)

    return LogEntry(tree=tree, parent=parent, message=message)


# function to ignore file:

def is_ignored(path):
    """Check if a path should be ignored.
    
    Args:
        path (str): Path to check
    
    Returns:
        bool: True if path should be ignored, False otherwise
    
    Ignores:
    - .git and .mygit directories
    - .gitignore files
    - __pycache__ and *.egg-info
    """
    # Normalize path separators to handle both Windows and Unix paths
    path = path.replace('\\', '/')
    parts = path.split('/')

    #Files to ignore
    ignore_files = [
        '.git',
        '.mygit',
        '.gitignore',
        '__pycache__',
        '*.egg-info'
    ]
    # Check if any part of the path should be ignored
    if any(part in ignore_files for part in parts):
        return True
    
    if parts[-1] in ['.gitignore']:
        return True
    
    # Also ignore the entire .git and .mygit directories and their contents
    if '.git/' in path or '.mygit/' in path:
        return True
        
    return False
