# Configure repositories of the Serlo GitHub organization

This repo contains the utility script
[`./configure-repositories.py`](./configure-repositories.py) which configures a
repository based on predefined rules. It is used mainly for repositories of the
[Serlo GitHub organization](https://github.com/serlo).

## Usage

Run the script `./configure-repositories.py` with one or more paths to
repositories:

```bash
./configure-repositories.py [option ...] repo_path [repo_path ...]
```

Via `option` you can define the changes which shall be applied to the
repository. Run the following command to see the list of all possible rules:

```bash
./configure-repositories.py --help
```

### Example: Sort the yarn scripts alphabetically

```bash
./configure-repositories.py --sort-yarn-scripts ../api.serlo.org
```

### Example: Configure a local MySQL database

```bash
./configure-repositories.py --setup-local-mysql ../db-migrations
```

## Development

* Install the Python version in [.tool-versions](.tool-versions)
  * You may use [asdf](https://asdf-vm.com/) for the installation.
* Install [pipenv](https://pipenv.pypa.io/en/latest/installation/#installing-pipenv)
* Run `pipenv install --dev` to install the dev dependencies.
* Run `pipenv shell` to activate the project's [virtual environment](https://docs.python.org/3/library/venv.html).
* Run `pipenv run lint` to run the linting