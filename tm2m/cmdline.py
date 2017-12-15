

import argparse

def commandline():
    main(generate_args())


def generate_args(in_args=None):
    parser = argparse.ArgumentParser()
    add_arg = parser.add_argument
    add_arg('--version', action='store_true')
    return parser.parse_args(in_args)

def main(args):
    return "tm2m"
