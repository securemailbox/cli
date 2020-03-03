import click
import pprint
import sys
import re
from pathlib import Path
from os import getlogin
from gpgopt import GpgOpt

@click.group()
@click.pass_context
def client(ctx):
    """Initial gnupg."""
    # Set config file path.
    config_path = Path('scmail.conf')
    ctx.obj['config'] = config_path

    # If the config not exist, set user information. If not, run initial gpg.
    if config_path.exists() == False:
        gnupghome, email = ctx.invoke(set_user_info)
    else:
        gnupghome, email = load_config()

    ctx.obj['gpg'] = GpgOpt(mygnupghome=gnupghome, email=email)

@click.pass_context
def load_config(ctx):
    """Load config file."""

    print("Now, laod previous config file:")
    f = ctx.obj['config'].open('r').read()
    config = re.split('\n|=', f)

    for i in range(0, len(config), 2):
        print('The {} is: {}'.format(config[i], config[i+1]))

    return (config[1], config[3])

@click.command()
@click.pass_context
def choose_primary_key(ctx):
    pass

@click.command()
@click.option('--gnupghome', prompt='Enter your gnupg home dir:', default='gnupgkeys', help='The home dir of gnupg key pairs.')
@click.option('--email', prompt='Enter your email:', default=getlogin()+'@scmail.dev', help='The email of user.')
@click.pass_context
def set_user_info(ctx, gnupghome, email):
    """Set user information and return gnupghome and email."""
    config = 'gnupghome=' + gnupghome + '\n' + 'email=' + email

    # Store config file and other information.
    ctx.obj['config'].touch()
    with ctx.obj['config'].open('w') as f:
        f.write(config)

    return (gnupghome, email)

@click.command()
@click.option('--key-type', prompt='Enter key type:', default="RSA", help='The algorithms to generate the key. ex. RSA')
@click.option('--key-length', prompt='Enter key length:', default=1024, help='The length of the key.')
@click.option('--expire-date', prompt='Enter expire date:', default="2y", help='The expire time of the key pair.')
@click.password_option('--password', prompt='Enter private key password:', help='Password of private key.')
@click.pass_context
def create_key(ctx, key_type, key_length, expire_date, password):
    """Create gnupg key pairs."""
    print('Those are the information about the key will be created:\n')
    ctx.obj['gpg'].create(password, key_type=key_type, key_length=key_length, expire_date=expire_date)

@click.command()
@click.option('--show-private', prompt='Do you want to show the private keys?', default=False, is_flag=True, help='Whether show the private keys')
@click.pass_context
def list_keys(ctx, show_private):
    """List and print all the keys in the gnupg home dir."""
    keys = ctx.obj['gpg'].list_keys(show_private)
    print('You have {} keys.'.format(len(keys)))
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(keys)
    pp.pprint(ctx.obj['gpg'].key)

@click.command()
# @click.option('--is-this-email', prompt='Do you want to user your default email as sender?\n{}'.format('x'), default=True, is_flag=True, help='Whether sender email is your default email.')
@click.pass_context
def register(ctx, is_this_email):
    """Register scmail.
    """
    # Request register.


@click.command()
@click.pass_context
def send(ctx):
    # Choose recipients
    ctx.invoke(list_keys, Content=False)
    pass

@click.command()
@click.pass_context
def retrieve(ctx):
    pass

client.add_command(set_user_info)
client.add_command(create_key)
client.add_command(list_keys)
client.add_command(send)

if __name__=='__main__':
    client(obj={})
