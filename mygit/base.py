from . import data
import os
from collections import namedtuple

# Create the main function for write-tree commands.

def write_tree (directory='.'):
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

''' Deleting the current directory in reading to get the all from tree-read 
 again for that Version. '''

def _empty_current_directory():
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
    _empty_current_directory()
    for path, oid in get_tree (tree_oid, base_path='./').items ():
        os.makedirs (os.path.dirname (path), exist_ok=True)
        with open (path, 'wb') as f:
            f.write (data.get_object (oid))

# Create the main commit message function 

def commit(message):
    '''
    Take message as argument. Create the HASH object of that.
    Save it as HEAD into HEAD file.
    Return:
        The oid of the commit message.
    '''
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
    '''
        It extracts the commit information from commit objects.
        Returns: LogEntry tuple.
    '''
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
