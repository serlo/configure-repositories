#!/usr/bin/env python

import argparse
import json
import logging
import os
import shutil
import sys
import textwrap


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        os.path.basename(__file__),
        description="Configures repositories of the Serlo organisation",
    )

    parser.add_argument(
        "--setup-local-mysql", action="store_true", help="set up a local MySQL database"
    )
    parser.add_argument(
        "--setup-github-actions",
        action="store_true",
        help="Add default github actions for setting up Node.js and yarn",
    )
    parser.add_argument(
        "--sort-yarn-scripts",
        action="store_true",
        help="Sort yarn scripts alphabetically",
    )
    parser.add_argument("repo_path", nargs="+")

    args = parser.parse_args()

    for repo in args.repo_path:
        configure(repo, args)


def configure(repo, args):
    if not os.path.isdir(os.path.join(repo, ".git")):
        error(f"path {repo} is no git repository")

    if args.setup_local_mysql:
        setup_local_mysql_database(repo)

    if args.sort_yarn_scripts:
        sort_yarn_scripts(repo)

    if args.setup_github_actions:
        mirror_file(repo, os.path.join(".github", "actions"))


def sort_yarn_scripts(repo):
    def format_package_json(package_json):
        if "scripts" not in package_json:
            return package_json

        package_json["scripts"] = dict(sorted(package_json["scripts"].items()))

        return package_json

    update_package_json(repo, format_package_json)


def setup_local_mysql_database(repo):
    mirror_file(repo, "scripts/mysql")

    update_file(
        os.path.join(repo, "docker-compose.yml"),
        block_in_file(
            block=textwrap.dedent(
                """
                    mysql:
                      image: eu.gcr.io/serlo-shared/serlo-mysql-database:latest
                      platform: linux/x86_64
                      ports:
                        - '3306:3306'
                """
            ),
            start_marker="# START: MySQL service",
            end_marker="# END: MySQL service",
            indent_prefix="  ",
        ),
        default_content=textwrap.dedent(
            """
                version: '3.9'

                services:
            """
        ),
    )

    def update(package_json):
        package_json.setdefault("scripts", {})

        ts_node_cmd = "ts-node --experimental-specifier-resolution=node"
        package_json["scripts"].update(
            {
                "mysql": "docker compose exec mysql serlo-mysql",
                "mysql:dump": f"{ts_node_cmd} mysql/scripts/mysql-dump",
                "mysql:import-anonymous-data": f"{ts_node_cmd} mysql/scripts/mysql-import-anonymous-data",
                "mysql:rollback": f"{ts_node_cmd} mysql/scripts/mysql-rollback",
                "start:docker": "docker compose up --detach",
                "stop:docker": "docker compose down",
            }
        )

        if "start" not in package_json["scripts"]:
            package_json["scripts"]["start"] = "yarn start:docker"

        if "stop" not in package_json["scripts"]:
            package_json["scripts"]["stop"] = "yarn stop:docker"

        return package_json

    update_package_json(repo, update)

    remove_legacy_files(repo, ["docker-entrypoint-initdb.d"])


def update_package_json(repo, update_func):
    update_file(os.path.join(repo, "package.json"), update_json(update_func))


def mirror_file(repo, file):
    source_path = os.path.join(configuration_repo(), "files", file)
    target_path = os.path.join(repo, file)

    mirror_directories(source_path, target_path)


def remove_legacy_files(repo, files):
    for file in files:
        delete_recursively(os.path.join(repo, file))


def configuration_repo():
    return os.path.dirname(os.path.abspath(__file__))


def update_json(update_func):
    def update_file_content(content):
        current_json = json.loads(content)

        new_json = update_func(current_json)

        return json.dumps(new_json, sort_keys=False, indent=2) + "\n"

    return update_file_content


def block_in_file(block, start_marker, end_marker, indent_prefix=""):
    def update_file_content(content):
        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        new_content = (
            "\n" + indent_prefix + start_marker if start_index < 0 else start_marker
        )
        new_content += textwrap.indent(block, indent_prefix)
        new_content += "\n" if not block.endswith("\n") else ""
        new_content += indent_prefix + end_marker + "\n"

        start_index = len(content) if start_index < 0 else start_index
        end_index = len(content) if end_index < 0 else end_index + len(end_marker) + 1

        return content[0:start_index] + new_content + content[end_index:]

    return update_file_content


def update_file(file_path, update_func, default_content=None):
    content = read_file(file_path)
    content = default_content if content == None else content

    if content == None:
        return

    new_content = update_func(content)

    write_to_file(file_path, new_content)


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


def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        error(f"Error occurred while reading the file: {file_path}\n{e}")


def write_to_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        error(f"Error occurred while writing to file: {file_path}\n{e}")


def error(message):
    logging.error(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
