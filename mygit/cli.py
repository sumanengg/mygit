import argparse
from . import data
import os

def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()
    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

def init(args):
    data.init()
    print (f'Initialized empty ugit repository in {os.getcwd()}/{data.GIT_DIR}')

if __name__ == "__main__":
    main()