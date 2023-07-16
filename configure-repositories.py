#!/usr/bin/env python

import json
import logging
import os
import shutil
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

    if settings.get("localMysqlDatabase", False):
        setup_local_mysql_database(repo)


def setup_local_mysql_database(repo):
    mirror_file(repo, "mysql")

    remove_legacy_files(repo, ["docker-entrypoint-initdb.d"])


def mirror_file(repo, file):
    source_path = os.path.join(configuration_repo(), "files", file)
    target_path = os.path.join(repo, file)

    mirror_directories(source_path, target_path)


def remove_legacy_files(repo, files):
    for file in files:
        delete_recursively(os.path.join(repo, file))


def configuration_repo():
    return os.path.dirname(os.path.abspath(__file__))


def mirror_directories(source_path, target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)


def delete_recursively(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    except Exception as e:
        error(f"Error occurred while deleting: {path}\n{e}")


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
