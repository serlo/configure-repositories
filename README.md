# Configure repositories of the Serlo GitHub organization

This repo contains the utility CLI `configure-repositories` that configures a
repository based on predefined rules. It is used mainly for repositories of the
[Serlo GitHub organization](https://github.com/serlo).

## Usage

Run the script `python configure-repositories.py` with one or more paths to
repositories:

```bash
python configure_repositories.py [OPTIONS] COMMAND REPO
```

Via `COMMAND` you can define the changes which shall be applied to the
repository. Run any of the following commands to see the list of all possible commands:

```bash
python configure_repositories.py --help
```


```bash
python configure_repositories.py
```

### Example: Sort the yarn scripts alphabetically

```bash
python configure_repositories.py sort-yarn-scripts ../api.serlo.org
```

### Example: Configure a local MySQL database

```bash
python configure_repositories.py setup-local-mysql ../db-migrations
```

## Development

* Install the Python version in [.tool-versions](.tool-versions)
  * You may use [asdf](https://asdf-vm.com/) for the installation.
* Install [pipenv](https://pipenv.pypa.io/en/latest/installation/#installing-pipenv)
* Run `pipenv install --dev` to install the dev dependencies.
* Run `pipenv shell` to activate the project's [virtual environment](https://docs.python.org/3/library/venv.html).
* Run `pipenv run lint` to run the linting