# cli

A command line client for interacting a secure mailbox

## Requirements

- [click](https://click.palletsprojects.com/en/7.x/)
- [python-gnupg](https://pythonhosted.org/python-gnupg/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [requests](https://requests.readthedocs.io/en/master/)

## Getting Started

### API

Before use this application, install and run [api](https://github.com/securemailbox/api).

### CLI

```bash
# To download and install
pyenv install 3.8.1

# To use
pyenv global 3.8.1

# To check
python --version # Python 3.8.1

# To install other requirements
pipenv install
```

## Features

### Create key

```bash
pipenv run python scmail.py create-key
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
pipenv run python sc_mail.py register
```

options:

- fingerprint: user's fingerprint

### Retrieve

```bash
pipenv run python sc_mail.py retrieve
```

options:

- fingerprint: user's fingerprint
- password: the password of private key.

### Send

```bash
pipenv run python sc_mail.py send
```

options:

- recipient: the fingerprint of recipient.
- message: the message should be sent.

### List key

```bash
pipenv run python sc_mail.py list_keys
```

options:

- show_private: whether the output are private keys.

### Help

Help about all commands.

```bash
pipenv run python scmail.py --help

# or all options about one command.
pipenv run python sc_mail.py [command] --help
```
