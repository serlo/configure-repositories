#!/usr/bin/env python

import json
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

    package_json_file = os.path.join(repo, "package.json")

    try:
        package_json = read_json_file(package_json_file)
    except FileNotFoundError:
        error(f"{package_json_file} does not exist")
    except json.decoder.JSONDecodeError:
        error(f"{package_json_file} is no json file")

    settings = package_json.get("settings", None)

    if settings == None:
        logging.warn(f"{package_json_file} does not have a key 'settings'")
        return


def read_json_file(json_file):
    with open(json_file, "r") as fd:
        return json.load(fd)


def help():
    print("Usage: ./configure-repositories.py <path1> [<path2>...]", file=sys.stderr)


def error(message):
    logging.error(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
