import requests
import click
import pprint
import sys
import re
from pathlib import Path
from os import getlogin
import json
from gpgopt import GpgOpt

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
    ctx.obj['pp'].pprint(key.__dict__)


@click.command()
@click.option('--show-private', prompt='Do you want to show the private keys?', default=False, is_flag=True,
              help='Whether show the private keys')
@click.pass_context
def list_keys(ctx, show_private):
    """List and print all the keys in the gnupg home dir."""
    keys = ctx.obj['gpg'].list_keys(show_private)
    key_type = 'public' if show_private is False else 'private'
    print('You have {} {} keys.'.format(len(keys), key_type))
    ctx.obj['pp'].pprint(keys.__dict__)


@click.command()
@click.pass_context
def register(ctx):
    """Register sc_mail API."""
    # Request register.
    fingerprint = ctx.obj['gpg'].list_keys(True).curkey.get('fingerprint')
    data = {'fingerprint': fingerprint}

    # Register
    r = requests.post("http://127.0.0.1:8080/register/")
    print(r.text)

    if 'success' in r:
        print('Registration success.')
    else:
        print('Registration fail.\nError is: {}'.format(r.get("error")))


@click.command()
@click.option('--recipient', prompt='The recipient', required=True, help='The email address of the recipient.')
@click.password_option('--password', prompt='Enter passwordo of private key to decrypt', help='The passphrase of private key')
@click.pass_context
def retrieve(ctx, recipient, password):
    """Retrieve and Post messages from API"""
    # Retrieve
    r = requests.post("http://127.0.0.1:8080/retrieve/")
    # Get response
    res = json.loads(r)
    # print(res)
    if 'success' in res:
        print('The message retrieve successful.')
    else:
        print('The message retrieve fail.\nError is: {}'.format(res.get("error")))
        # return

    # Decrypt the messages.
    ok, messages = ctx.obj['gpg'].decrypt_message(messages=res, passphrase=password)
    ctx.obj['pp'].pprint(messages[:-1])
    if ok is False:
        print('Other message decrypt fail.\n{}'.format(messages[-1]))
    else:
        ctx.obj['pp'].pprint(messages[-1])
        print('Decrypt message successful.')


@click.command()
@click.option('--recipient', prompt='The recipient email', required=True, help='The email of the recipient.')
@click.option('--message', required=True, prompt='The message', help='Message that will send.')
@click.pass_context
def send(ctx, recipient, message):
    """Send a message."""
    # Choose recipient and Encrypted
    ok, encrypted_message = ctx.obj['gpg'].encrypt_message(message, recipient)
    if ok is False:
        print('Message encrypt fail.\n{}'.format(encrypted_message))
    else:
        print('Message encrypt success.')

    # Send
    payload = {'fingerprint': recipient, 'message': message}
    r = requests.post("http://127.0.0.1:8080/send/", json=payload)
    r = json.loads(r)
    print(r.text)


@click.command()
@click.option('--fingerprint', prompt='Enter the fingerprint of that key', required=True, help='The fingerprint of exported key.')
@click.option('--is-file', prompt='Do you want to store keys to file (or print)?', is_flag=True, help='Whether export to file.')
@click.option('--is-pvt', prompt='Do you want to export private key?', is_flag=True, help='Whether export private keys.')
@click.pass_context
def export_key(ctx, fingerprint, is_file, is_pvt):
    file_name = None
    passphrase = None

    if is_file is True:
        file_name = click.prompt('Enter the file name', type=str)
        file_name = Path(file_name)
        if file_name.exists() is False:
            file_name.touch()

    if is_pvt is True:
        passphrase = click.prompt('Enter pvt\'s passphrase', hide_input=True, type=str)

    pub, pvt = ctx.obj.get('gpg').export_key(fingerprint, export_pvt=is_pvt, password=passphrase, to_file=is_file, path=file_name)

    if is_file is False:
        ctx.obj.get('pp').pprint(pub, pvt)


# client.add_command(update_user_info)
client.add_command(create_key)
client.add_command(list_keys)
client.add_command(register)
client.add_command(send)
client.add_command(retrieve)
client.add_command(export_key)


if __name__ == '__main__':
    client(obj={})
