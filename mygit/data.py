import os
import hashlib

GIT_DIR = ".mygit"

def init():
    try:
        os.makedirs(GIT_DIR, exist_ok=True)
        os.makedirs(f'{GIT_DIR}/objects', exist_ok=True)
    except Exception as e:
        raise

def hash_object(data, obj_type="blob"):
    try:
        header = f"{obj_type}\0".encode()
        full_data = header + data
        oid = hashlib.sha1(full_data).hexdigest()
        with open(f'{GIT_DIR}/objects/{oid}', 'wb') as f:
            f.write(full_data)
        return oid
    except Exception as e:
        raise

# get_object now returns (type, data)
def get_object(oid, type="blob"):
    try:
        with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
            full_data = f.read()
        obj_type, _, data = full_data.partition(b'\0')
        type_ = obj_type.decode()
        if type is not None:
            assert type_ == type, f'Expected {type}, got {type_}'
        return data
    except Exception as e:
        raise