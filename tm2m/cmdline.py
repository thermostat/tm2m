

import argparse
import sys
from . import named_histories

__version__ = '0.1'

def commandline():
    main(generate_args())


def generate_args(in_args=None):
    parser = argparse.ArgumentParser()
    add_arg = parser.add_argument
    add_arg('--version', action='store_true')
    add_arg('--history', action='store_true')
    add_arg('--add-stdin', action='store_true')
    add_arg('--search', nargs=1)
    add_arg('--name', nargs=1)
    add_arg('--nbr-prefix', action='store_true', default=False)
    return parser.parse_args(in_args)

def main(args):
    if args.version:
        print("tm2m version {}".format(__version__))
        sys.exit(0)
    if args.add_stdin:
        named_histories.add_fd(args.name[0],
                               sys.stdin, args.nbr_prefix)
    elif len(args.search):
        named_histories.search(args.name[0], args.search[0])
            

def history_add_cmd(args):
    pass
