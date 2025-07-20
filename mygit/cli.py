import argparse
from . import data, base
import os, sys

def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()
    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)
    hash_object_parcer = commands.add_parser("hash-object")
    hash_object_parcer.add_argument("file")
    hash_object_parcer.set_defaults(func=hash_function)
    # cat-file to get the object 
    cat_file_parcer = commands.add_parser("cat-file")
    cat_file_parcer.add_argument("oid")
    cat_file_parcer.set_defaults(func=cat_file)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

def init(args):
    data.init()
    print (f'Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}')

# Hash_function to take file as argument and stroed it as content-addressble

def hash_function(args):
    try:
        with open(args.file, 'rb') as f:
            data.hash_object(f.read())
    except Exception as e:
        raise

# get_object function is used to get the object using oid of the file, loaded earlier

def cat_file(args):
    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(data.get_object(args.oid))
    except Exception as e:
        raise

if __name__ == "__main__":
    main()