# cli

A command line client for interacting a secure mailbox

[![Build Status](https://www.travis-ci.org/securemailbox/cli.svg?branch=develop)](https://www.travis-ci.org/securemailbox/cli)

[![codecov](https://codecov.io/gh/securemailbox/cli/branch/develop/graph/badge.svg)](https://codecov.io/gh/securemailbox/cli)

## Requirements

- [python 3](https://www.python.org/downloads/)
- [poetry](https://python-poetry.org/)

Note: Additional required packages can be found in [pyproject.toml](./pyproject.toml).

## Getting Started

#### Installation

Recommended installation of python and associated packages:

Installing python can be easily done with [pyenv](https://github.com/pyenv/pyenv#installation) (unless you're on windows)

```bash
# To download and install
pyenv install 3.8.1

# To use
pyenv global 3.8.1

# To check
python --version # Python 3.8.1
```

Project dependencies can be installed with either `poetry`, `pipenv` or `pip`.
We recommend using poetry.

```bash
# Upgrade pip and setuptools to ensure we can build libraries against 3.8
python -m pip install --upgrade pip setuptools

# Install poetry and project dependencies
python -m pip install poetry && poetry install
```

Full documentation for installing and running via other supported tools can be found [in the wiki](https://github.com/securemailbox/api/wiki/Development-environment-setup)

Other tools used in development:

```bash
# Install the black formatting tool
# Note: Install to global package list
# Docs: https://black.readthedocs.io/en/stable/
python -m pip install --user black
```

##### API

This application is intended to interact with the secure mailboxes API.
To install and run it, please see the API repositories [README](https://github.com/securemailbox/api/blob/develop/README.md).

## Features

### Create key

```bash
poetry run python scmailclient create-key
```

options:

- name
- email
- key_type
- key_length
- expire_date
- password

### Register

```bash
poetry run python scmailclient register
```

options:

- fingerprint: user's fingerprint

### Retrieve

```bash
poetry run python scmailclient retrieve
```

options:

- fingerprint: user's fingerprint.
- sender_fingerprint: optional, sender's fingerprint.
- password: the password of private key.

### Send

```bash
poetry run python scmailclient send
```

options:

- recipient: the fingerprint of recipient.
- message: the message should be sent.

### List key

```bash
poetry run python scmailclient list_keys
```

options:

- show_private: whether the output are private keys.

### Help

Help about all commands.

```bash
poetry run python scmailclient --help

# or all options about one command.
poetry run python scmailclient [command] --help
```

### Testing

Install pytest for our premade tests.
If you installed everything in the pipfile pytest should already be installed.

```bash
poetry add pytest --dev
```

##### Basic testing

```bash
poetry run pytest
```

This will run tests with filenames that start with 'test\_'.

##### Testing with Coverage

```bash
# Only collect coverage info for our app and generate branch coverage
poetry run coverage run -m pytest

poetry run coverage report

# Show lines missing coverage
poetry run coverage report -m
```

### Formatting

This repository uses [black](https://github.com/psf/black) to format its files. You can read more about it [here](https://black.readthedocs.io/en/stable/)

To run black on the project:

```bash
# To check which files would be updated
black --check .

# To run black on the whole repo
black .
```
