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
pipenv run python scmail.py register
```

options:

- fingerprint: user's fingerprint

### Retrieve

```bash
pipenv run python scmail.py retrieve
```

options:

- fingerprint: user's fingerprint.
- sender_fingerprint: optional, sender's fingerprint.
- password: the password of private key.

### Send

```bash
pipenv run python scmail.py send
```

options:

- recipient: the fingerprint of recipient.
- message: the message should be sent.

### List key

```bash
pipenv run python scmail.py list-keys
```

options:

- show_private: whether the output are private keys.

### Help

Help about all commands.

```bash
pipenv run python scmail.py --help

# or all options about one command.
pipenv run python scmail.py [command] --help
```

## Testing

### Two clients

1. Clone this repository into two different directories.

2. We recommend having two terminal windows open (one for each directory).

3. Create a key for each client. In each directory, run:
    ```
    pipenv run python scmail.py create-key
    ```
    * Feel free to name one Alice and the other Bob.
    * Same for email, e.g., alice@scmail.dev.
    * Go ahead and accept the defaults (press enter) when prompted for key type, key length, and expire date.
    * Create a password for each. For testing purposes, how about "a" for Alice and "b" for Bob?

4. Keep track of each client's fingerprint. If you happen to forget, view again with:
    ```
    pipenv run python scmail.py list-keys
    ```

5. Register each client's fingerprint. Run:
    ```
    pipenv run python scmail.py register
    ```
    * When prompted, enter the fingerprint to register.

6. In order to send messages to one another, each client must import the other's public key info (to encrypt the message with the recipient's public key). Export each client's public key using:
    ```
    pipenv run python scmail.py export-key
    ```
    * Enter the fingerprint of the client to export.
    * Enter "y" when prompted to export to a file.
    * Enter "n" when prompted to export the private key.
    * Give the file a name, e.g., alicePubKey.

7. For each client, import the other's public key file. Run:
    ```
    pipenv run python scmail.py import-key
    ```
    * Enter the path of the file to import (or move the file into the current directory and just enter the file name).
    * Enter the fingerprint of the client to import.
    * Verify the import was successful using `list-keys`.

8. Send a message from one client to another. Run:
    ```
    pipenv run python scmail.py send
    ```
    * Enter the sender's fingerprint (who the message is coming from).
    * Enter the recipient's fingerprint (who the message is going to).
    * Enter the message to send.

9. Retrieve messages sent to a client. Run:
    ```
    pipenv run python scmail.py retrieve
    ```
    * Enter the fingerprint of the client whose messages you'd like to retrieve.
    * Enter the sender's fingerprint to view messages only sent by that client. Or don't provide any sender fingerprint to view all messages.
    * Enter the private key password in order to decrypt the message(s).
    * Note: a client can only decrypt messages if they have the recipient's private key, i.e., even if a user knows a cient's password, they still need their private key to actually decrypt messages. E.g., Alice cannot decrypt messages sent to Bob, because Alice doesn't know Bob's private key. Bob could however export his private key info and send it to Alice to import, allowing her to decrypt messages sent to Bob. Although, this is oftentimes not a desired use case.