import requests
import click
import pprint
import sys
import re
from pathlib import Path
from os import getlogin
import json
from gpgopt import GpgOpt

# for test
import request

# Import when api cannot used.
from random import getrandbits


@click.group()
@click.pass_context
def client(ctx):
    """Initial gnupg."""
    # Set config file path.
    config_path = Path('scmail.conf')
    ctx.obj['config'] = config_path

    # If the config not exist, set user information. If not, run initial gpg.
    if config_path.exists() is False:
        gnupghome, email = ctx.invoke(set_user_info, gnupghome=click.prompt('Enter your gnupg home dir:', default='gnupgkeys'), email=click.prompt('Enter your email:', default=getlogin() + '@scmail.dev'))
    else:
        gnupghome, email = load_config()

    ctx.obj['gpg'] = GpgOpt(mygnupghome=gnupghome, email=email)
    # Initial pretty printer
    ctx.obj['pp'] = pprint.PrettyPrinter(indent=2)


@click.pass_context
def load_config(ctx):
    """Load config file."""
    print("Now, laod previous config file:")
    f = ctx.obj['config'].open('r').read()
    config = re.split('\n|=', f)

    for i in range(0, len(config), 2):
        print('The {} is: {}'.format(config[i], config[i + 1]))

    print('\n')
    return config[1], config[3]


@click.command()
@click.pass_context
def choose_primary_key(ctx):
    pass


# @click.command()
@click.pass_context
def set_user_info(ctx, gnupghome, email):
    """Set user information and return gnupghome and email."""
    config = 'gnupghome=' + gnupghome + '\n' + 'email=' + email

    # Store config file and other information.
    ctx.obj['config'].touch()
    with ctx.obj['config'].open('w') as f:
        f.write(config)

    return gnupghome, email


@click.command()
@click.option('--gnupghome', prompt='Enter your gnupg home dir', default='gnupgkeys',
              help='The home dir of gnupg key pairs.')
@click.option('--email', prompt='Enter your email', default=getlogin() + '@scmail.dev', help='The email of user.')
@click.pass_context
def update_user_info(ctx, gnupghome, email):
    """Update gnupg home dir and personal email"""
    pass


@click.command()
@click.option('--key-type', prompt='Enter key type', default="RSA", help='The algorithms to generate the key. ex. RSA')
@click.option('--key-length', prompt='Enter key length', default=1024, help='The length of the key.')
@click.option('--expire-date', prompt='Enter expire date', default="2y", help='The expire time of the key pair.')
@click.password_option('--password', prompt='Enter private key password', help='Password of private key.')
@click.pass_context
def create_key(ctx, key_type, key_length, expire_date, password):
    """Create gnupg key pairs."""
    print('Those are the information about the key will be created:\n')
    ctx.obj['pp'].pprint({'email': ctx.obj['gpg'].email, 'key type': key_type, 'key length': key_length, 'expire date': expire_date})
    print('\n')
    key = ctx.obj['gpg'].create(password, key_type=key_type, key_length=key_length, expire_date=expire_date)
    # ctx.obj['pp'].pprint(key.__dict__)
    # ctx.obj['pp'].pprint(key.__doc__)


@click.command()
@click.option('--show-private', prompt='Do you want to show the private keys?', default=False, is_flag=True,
              help='Whether show the private keys')
@click.pass_context
def list_keys(ctx, show_private):
    """List and print all the keys in the gnupg home dir."""
    keys = ctx.obj['gpg'].list_keys(show_private)
    key_type = 'public' if show_private is False else 'private'
    print('You have {} {} keys.'.format(len(keys), key_type))
    # ctx.obj['pp'].pprint(keys.__dict__)
    # print('\n')


@click.command()
@click.pass_context
def register(ctx):
    """Register sc_mail API."""

    # Request register.
    fingerprint = 'a'
    r = {'fingerprint': fingerprint}
    res = json.loads(random_response())
    if 'success' in res:
        print('Registration success.')
    else:
        print('Registration fail.\nError is: {}'.format(res['error']))

    # Register
    r = requests.post("http://127.0.0.1:8080/register/")
    print(r.text)


@click.command()
@click.option('--recipient', prompt='The recipient', required=True, help='The email address of the recipient.')
@click.pass_context
def retrieve(ctx, recipient):
    """Retrieve messages from API"""

    # Choose recipients
    ctx.invoke(list_keys, show_private=False)

    # Get response
    res = json.loads(random_response())

    # print(res)
    if 'success' in res:
        print('The message retrieve successful.')
    else:
        print('The message retrieve fail.\nError is: {}'.format(res["error"]))
    
    #ctx['pp'].pprint(res)

    # Retrieve
    r = requests.post("http://127.0.0.1:8080/retrieve/")
    print(r.text)


@click.command()
@click.option('--recipient', prompt='The recipient', required=True, help='The fingerprint of the recipient.')
@click.option('--message', required=True, prompt='The message', help='Message that will send.')
@click.pass_context
def send(ctx, recipient, message):
    """Send a message."""

    # Choose recipient and Encrypted
    #encrypted_message = ctx['gpg'].encrypt_message(message, recipient)
    #if encrypted_message['ok'] is not True:
    #    print('Error.')

    # Send
    payload = {'fingerprint': recipient, 'message': message}
    r = requests.post("http://127.0.0.1:8080/send/", json=payload)
    print(r.text)


# client.add_command(update_user_info)
client.add_command(create_key)
client.add_command(list_keys)
client.add_command(register)
client.add_command(send)
client.add_command(retrieve)


def random_response():
    """Random response whether a api request is successful.
    Only used when API is not finish.
    """
    succ = getrandbits(1)
    js = {}
    if succ == 1:
        js['success'] = 1
    else:
        js['error'] = 'Not found'

    return json.dumps(js)


if __name__ == '__main__':
    client(obj={})
