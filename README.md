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
pipenv run python scmailclient create
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
pipenv run python scmailclient register
```

options:

- fingerprint(`-f`): user's fingerprint

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
pipenv run python scmailclient retrieve
```

options:

- fingerprint(`-f`): user's fingerprint.
- sender-fingerprint(`-s`): optional, sender's fingerprint.
- password(`-p`): the password of private key.

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
pipenv run python scmailclient send
```

options:

- sender-fingerprint(`-s`): the fingerprint of sender.
- recipient(`-r`): The fingerprint of recipient.
- message(`-m`): the message should be sent.

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
pipenv run python scmailclient list
```

options:

- private(`-p`): whether the output are private keys.

```
# result
2020-05-11 13:39:04,704 root INFO The gnupghome is: gnupgkeys
2020-05-11 13:39:04,705 root INFO Config file exists. Load Successful.
2020-05-11 13:39:04,709 gpgopt INFO Initialize GnuPG successful.
2020-05-11 13:39:04,710 root INFO Initialize client successful.
Do you want to show the private keys? [y/N]: y
2020-05-11 13:39:06,662 root INFO 3 private keys exist.
Current key is:

        Key ID:         90016092EB8B1804
        Fingerprint:    B1C9FFC5546D41F3E25B66EE90016092EB8B1804
        Length:         4096
        Trust Level:    u
        User Info:      Mike <mike@outlook.com>

Print all keys:

        Key ID:         27DF7944E90696FF
        Fingerprint:    8EB7CD394313135528D9182727DF7944E90696FF
        Length:         1024
        Trust Level:    u
        User Info:      dgu <dgu@scmail.dev>


        Key ID:         F9F076A576818B02
        Fingerprint:    5A814B6F491F094F41A70A95F9F076A576818B02
        Length:         2048
        Trust Level:    u
        User Info:      John <john@gmail.com>


        Key ID:         90016092EB8B1804
        Fingerprint:    B1C9FFC5546D41F3E25B66EE90016092EB8B1804
        Length:         4096
        Trust Level:    u
        User Info:      Mike <mike@outlook.com>

2020-05-11 13:39:06,663 root INFO List keys finished.
```

### Help

Help about all commands.

```bash
pipenv run python scmail.py --help

# or all options about one command.
pipenv run python scmail.py [command] --help
```
