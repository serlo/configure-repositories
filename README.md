# Configure repositories of the Serlo GitHub organization

This repo contains the utility CLI `configure-repositories` that configures a
repository based on predefined rules. It is used mainly for repositories of the
[Serlo GitHub organization](https://github.com/serlo).

## Installation

### Linux and Darwin (x86) 

Download the executable from the [Releases](https://github.com/serlo/configure-repositories/releases) and make it
executable: `chmod +x FILENAME`

### Windows and Darwin (arm64)

* Follow the steps in [Development](#development)
* Build the executable depending on the Platform:
  * Darwin arm64: `pipenv run build_darwin_arm64`
  * Windows: `pipenv run build_windows_x86`

## Usage

Run `./configure_repositories` with one or more paths to repositories:

```bash
./configure_repositories [OPTIONS] COMMAND REPO
```

Via `COMMAND` you can define the changes which shall be applied to the
repository. Run any of the following commands to see the list of all possible commands:

```bash
./configure_repositories --help
```


```bash
./configure_repositories
```

### Example: Sort the yarn scripts alphabetically

```bash
./configure_repositories sort-yarn-scripts ../api.serlo.org
```

### Example: Configure a local MySQL database

```bash
./configure_repositories setup-local-mysql ../db-migrations
```

## Development

* Install the Python version in [.tool-versions](.tool-versions)
  * You may use [asdf](https://asdf-vm.com/) for the installation.

### Using pipenv
* Install [pipenv](https://pipenv.pypa.io/en/latest/installation/#installing-pipenv)
* Run `pipenv install --dev` to install the dev dependencies.
* Run `pipenv shell` to activate the project's [virtual environment](https://docs.python.org/3/library/venv.html).
* Run `pipenv run lint` to run the linting

### Testing 

* You can test the commands running `python configure_repositories.py [OPTIONS] COMMAND REPO`

## Releases

* Change the version in [setup.py](setup.py)
* Push a new tag with the format `major.minor.patch`
* The push of a new tag will trigger the creation of the releases for:
  * [Linux (x86)](.github/workflows/release-linux.yml)
  * [macOS (x86)](.github/workflows/release-macos.yml)
