#!/usr/bin/env python

import logging
import os
import sys


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    args = sys.argv[1:]

    if len(args) == 0:
        error("No arguments specified!")

    if any(help_opt in args for help_opt in ["--help", "-h", "-?"]):
        help()
        sys.exit(0)

    for repo in args:
        configure(repo)


def configure(repo):
    if not os.path.isdir(repo):
        error(f"path {repo} is no directory")


def help():
    print("Usage: ./configure-repositories.py <path1> [<path2>...]", file=sys.stderr)


def error(message):
    logging.error(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
