#!/usr/bin/env python

import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    args = sys.argv[1:]

    if len(args) == 0:
        error("No arguments specified!")

    if any(help_opt in args for help_opt in ["--help", "-h", "-?"]):
        help()


def help():
    print_error("Usage: ./configure-repositories.py <path1> [<path2>...]")


def print_error(message):
    print(message, file=sys.stderr)


def error(message):
    logging.error(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
