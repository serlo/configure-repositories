import json
import os
import shutil
import textwrap
import click


@click.group()
def cli():
    """Configures repositories of the Serlo organisation"""


@cli.command("sort-yarn-scripts")
@click.argument("repo")
def sort_yarn_scripts(repo):
    """Sort yarn scripts alphabetically in the REPO"""

    validate_repo(repo)

    def format_package_json(package_json):
        if "scripts" not in package_json:
            return package_json

        package_json["scripts"] = dict(sorted(package_json["scripts"].items()))

        return package_json

    update_package_json(repo, format_package_json)


@cli.command("setup-local-mysql")
@click.argument("repo")
def setup_local_mysql_database(repo):
    """Set up a local MySQL database in the REPO"""

    validate_repo(repo)

    mirror_file(repo, os.path.join("scripts", "mysql"))

    update_file(
        os.path.join(repo, "docker-compose.yml"),
        block_in_file(
            block=textwrap.dedent(
                """
                    mysql:
                      image: eu.gcr.io/serlo-shared/serlo-mysql-database:latest
                      platform: linux/x86_64
                      pull_policy: always
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

        mysql_entrypoint_cmd = (
            'mysql sh -c "pv /docker-entrypoint-initdb.d/001-init.sql | serlo-mysql"'
        )
        package_json["scripts"].update(
            {
                "mysql": "docker compose exec mysql serlo-mysql",
                "mysql:import-anonymous-data": "./scripts/mysql/import-anonymous-data.sh",
                "mysql:rollback": f"docker compose exec {mysql_entrypoint_cmd}",
                "start:docker": "docker compose up --detach",
                "stop:docker": "docker compose down",
            }
        )

        package_json["scripts"].pop("mysql:dump", None)

        if "start" not in package_json["scripts"]:
            package_json["scripts"]["start"] = "yarn start:docker"

        if "stop" not in package_json["scripts"]:
            package_json["scripts"]["stop"] = "yarn stop:docker"

        return package_json

    update_package_json(repo, update)

    remove_legacy_files(
        repo,
        [
            "docker-entrypoint-initdb.d",
            os.path.join("scripts", "mysql", "mysql-dump.ts"),
            os.path.join("scripts", "mysql", "transform"),
        ],
    )


def validate_repo(repo):
    if not os.path.isdir(os.path.join(repo, ".git")):
        raise click.ClickException(f"path {repo} is no git repository")


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
    content = default_content if content is None else content

    if content is None:
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
        raise click.ClickException(f"Error occurred while deleting: {path}\n{e}")


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise click.ClickException(
            f"Error occurred while reading the file: {file_path}\n{e}"
        )


def write_to_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        raise click.ClickException(
            f"Error occurred while writing to file: {file_path}\n{e}"
        )


if __name__ == "__main__":
    cli()
