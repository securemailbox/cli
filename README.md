# cli

A command line client for interacting a secure mailbox

## Requirements

- [GPG](https://gnupg.org/)
- [click](https://click.palletsprojects.com/en/7.x/)
- [python-gnupg](https://pythonhosted.org/python-gnupg/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [requests](https://requests.readthedocs.io/en/master/)

## Getting Started

### API

This is a client for [api](https://github.com/securemailbox/api).

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


```
# result
Enter your gnupg home dir: [gnupgkeys]: mykeys
2020-05-11 13:07:33,947 root INFO Setting user information finish.
2020-05-11 13:07:33,959 gpgopt INFO Initialize GnuPG successful.
2020-05-11 13:07:33,960 root INFO Initialize client successful.
Enter Name [dgu]: John
Enter Email [dgu@scmail.dev]: john@gmail.com
Enter key type [RSA]: RSA
Enter key length [1024]: 2048
Enter expire date [2y]: 2y
Enter private key password:
Repeat for confirmation:
2020-05-11 13:08:38,147 root INFO Key Creation finished.
Fingerprint is A4229AFA03431561A7E0B7892312B160D4E4C715.
```

### Register

```bash
pipenv run python scmail.py register
```

options:

- fingerprint: user's fingerprint

```
# result
2020-05-11 13:12:36,234 root INFO The gnupghome is: mykeys
2020-05-11 13:12:36,234 root INFO Config file exists. Load Successful.
2020-05-11 13:12:36,238 gpgopt INFO Initialize GnuPG successful.
2020-05-11 13:12:36,239 root INFO Initialize client successful.
Register fingerprint: A4229AFA03431561A7E0B7892312B160D4E4C715
2020-05-11 13:12:47,313 root INFO begin register.
2020-05-11 13:12:48,235 root INFO Registration success.
Fingerprint is: A4229AFA03431561A7E0B7892312B160D4E4C715
```

### Retrieve

```bash
pipenv run python scmail.py retrieve
```

options:

- fingerprint: user's fingerprint.
- sender_fingerprint: optional, sender's fingerprint.
- password: the password of private key.

```
# result
2020-05-11 13:22:48,335 root INFO The gnupghome is: mykeys
2020-05-11 13:22:48,336 root INFO Config file exists. Load Successful.
2020-05-11 13:22:48,340 gpgopt INFO Initialize GnuPG successful.
2020-05-11 13:22:48,341 root INFO Initialize client successful.
Enter fingerprint of mailbox: 3FAC74D0F763750DA54781BD9A7B6BDA58825BF5
Enter the fingerprint of sender []: A4229AFA03431561A7E0B7892312B160D4E4C715
Enter password of private key:
Repeat for confirmation:
2020-05-11 13:22:54,799 root INFO The message retrieve successful.
Sending message example!
2020-05-11 13:22:54,969 root INFO Decrypt 1 message successful.
```

### Send

```bash
pipenv run python scmail.py send
```

options:

- recipient: the fingerprint of recipient.
- message: the message should be sent.

```
# result
2020-05-11 13:20:23,497 root INFO The gnupghome is: mykeys
2020-05-11 13:20:23,497 root INFO Config file exists. Load Successful.
2020-05-11 13:20:23,502 gpgopt INFO Initialize GnuPG successful.
2020-05-11 13:20:23,502 root INFO Initialize client successful.
The sender fingerprint: A4229AFA03431561A7E0B7892312B160D4E4C715
The recipient fingerprint: 3FAC74D0F763750DA54781BD9A7B6BDA58825BF5
The message: Sending message example!
2020-05-11 13:20:49,520 root INFO Message encrypt success.
2020-05-11 13:20:50,212 root INFO Sending message success.
```

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
