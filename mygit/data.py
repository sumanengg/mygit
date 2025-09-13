import os
import hashlib

GIT_DIR = ".mygit"


def init():
    """Initialize a new mygit repository.

    Creates the .mygit directory and objects subdirectory if they don't exist.

    Raises:
        Exception: If directory creation fails
    """
    try:
        os.makedirs(GIT_DIR, exist_ok=True)
        os.makedirs(f"{GIT_DIR}/objects", exist_ok=True)
    except Exception:
        raise


def hash_object(data, obj_type="blob"):
    """Store an object in the repository and return its hash.

    Args:
        data (bytes): The content to store
        obj_type (str): The type of object ('blob', 'tree', 'commit')

    Returns:
        str: The SHA-1 hash (OID) of the stored object

    Raises:
        Exception: If writing the object fails
    """
    try:
        header = f"{obj_type}\0".encode()
        full_data = header + data
        oid = hashlib.sha1(full_data).hexdigest()
        with open(f"{GIT_DIR}/objects/{oid}", "wb") as f:
            f.write(full_data)
        return oid
    except Exception:
        raise


def get_object(oid):
    """Retrieve an object from the repository.

    Args:
        oid (str): The object ID (SHA-1 hash) to retrieve
        expected_type (str, optional): Verify the object is of this type

    Returns:
        bytes: The object's data (without type header)

    Raises:
        AssertionError: If expected_type doesn't match actual type
        Exception: If reading the object fails
    """
    try:
        with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
            full_data = f.read()
        obj_type, _, data = full_data.partition(b"\0")
        return data
    except Exception:
        raise


# Set last commit hash as HEAD
def set_HEAD(oid):
    """Retrieve an object from the repository.

    Args:
        oid (str): The object ID (SHA-1 hash) to retrieve
        expected_type (str, optional): Verify the object is of this type

    Returns:
        bytes: The object's data (without type header)

    Raises:
        AssertionError: If expected_type doesn't match actual type
        Exception: If reading the object fails
    """
    try:
        with open(f"{GIT_DIR}/HEAD", "w") as f:
            f.write(oid)
    except Exception:
        raise


def get_HEAD():
    """Get the current HEAD commit.

    Returns:
        str: The object ID of the current HEAD commit
        None: If HEAD file doesn't exist (no commits yet)
    """
    try:
        if os.path.isfile(f"{GIT_DIR}/HEAD"):
            with open(f"{GIT_DIR}/HEAD", "r") as f:
                return f.read().strip()
    except Exception:
        raise
