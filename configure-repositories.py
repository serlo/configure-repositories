#!/usr/bin/env python

import sys


def main():
    args = sys.argv[1:]

    if len(args) == 0 or any(
        help_opt in args for help_opt in ["--help", "-h", "-?"]
    ):
        help()


def help():
    print_error("Usage: ./configure-repositories.py <path1> [<path2>...]")


def print_error(message):
    print(message, file=sys.stderr)


if __name__ == "__main__":
    main()
