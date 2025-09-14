import argparse
import os
import sys
import textwrap

from . import base
from . import data


def main():
    """Parse command line arguments and dispatch to appropriate function."""
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

    # write-tree command
    write_tree_parcer = commands.add_parser("write-tree")
    write_tree_parcer.set_defaults(func=write_tree)

    # read-tree command
    read_tree_parser = commands.add_parser("read-tree")
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument("tree")

    # Creating the commit
    commit_parser = commands.add_parser("commit")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument("-m", "--message", required=True)

    # Log
    log_parser = commands.add_parser("mylog")
    log_parser.set_defaults(func=log)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def init(args):
    """Initialize a new mygit repository in the current directory."""
    data.init()
    print(f"Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}")


# Hash_function to take file as argument and stroed it as content-addressble


def hash_function(args):
    """Store a file in the object database."""
    try:
        with open(args.file, "rb") as f:
            data.hash_object(f.read())
    except Exception:
        raise


# get_object function is used to get the object using oid of the file, loaded earlier


def cat_file(args):
    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(data.get_object(args.oid))
    except Exception:
        raise


def write_tree(args):
    """Create a tree object from the current directory state."""
    try:
        print(base.write_tree())
    except Exception:
        raise


def read_tree(args):
    try:
        base.read_tree(args.tree)
    except Exception:
        raise


def commit(args):
    try:
        print(base.commit(args.message))
    except Exception:
        raise


def log(args):
    oid = data.get_HEAD()
    while oid:
        commit = base.get_log(oid)
        print(f"Commit {oid}\n")
        print(textwrap.indent(commit.message, "    "))
        print("")
        oid = commit.parent


if __name__ == "__main__":
    main()
